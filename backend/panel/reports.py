"""Statistics, dues report and Excel exports for the panel."""
from datetime import date
from decimal import Decimal
from io import BytesIO

from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from content.models import Activity, Municipality
from dues.models import DuesRate, Payment
from events.models import Registration

from .registry import user_scope
from .views import scoped_events, scoped_members, staff_member_required

AGE_BANDS = [(16, 25), (26, 35), (36, 45), (46, 55), (56, 65), (66, 120)]


def bars(rows, key="value"):
    """Add a percentage width for CSS bar charts."""
    top = max((r[key] for r in rows), default=0) or 1
    for r in rows:
        r["pct"] = round(100 * r[key] / top)
    return rows


@staff_member_required
def stats(request):
    scope = user_scope(request.user)
    members = scoped_members(request)
    active = members.filter(status="active")
    today = date.today()

    by_muni = [
        {"label": m.name, "value": m.active, "pending": m.pending}
        for m in Municipality.objects.filter(**({"pk": scope.pk} if scope else {})).annotate(
            active=Count("memberprofile", filter=Q(memberprofile__status="active")),
            pending=Count("memberprofile", filter=Q(memberprofile__status="pending")),
        )
    ]
    top = max((r["value"] + r["pending"] for r in by_muni), default=0) or 1
    for r in by_muni:
        r["pct"] = round(100 * r["value"] / top)
        r["ppct"] = round(100 * r["pending"] / top)

    ages = []
    for lo, hi in AGE_BANDS:
        start = date(today.year - hi - 1, today.month, min(today.day, 28))
        end = date(today.year - lo, today.month, min(today.day, 28))
        ages.append({"label": f"{lo}–{hi if hi < 120 else '+'}", "value": active.filter(birth_date__gt=start, birth_date__lte=end).count()})
    bars(ages)

    twelve_months_ago = date(today.year - 1, today.month, 1)
    growth_raw = {
        r["m"].strftime("%Y-%m"): r["n"]
        for r in members.filter(created_at__date__gte=twelve_months_ago)
        .annotate(m=TruncMonth("created_at")).values("m").annotate(n=Count("id"))
    }
    growth = []
    y, mth = twelve_months_ago.year, twelve_months_ago.month
    for _ in range(13):
        k = f"{y}-{mth:02d}"
        growth.append({"label": k, "value": growth_raw.get(k, 0)})
        mth += 1
        if mth > 12:
            y, mth = y + 1, 1
    bars(growth)

    acts = Activity.objects.filter(**({"municipality": scope} if scope else {}))
    act_by_cat = bars([
        {"label": dict(Activity.CATEGORY)[r["category"]], "value": r["n"]}
        for r in acts.values("category").annotate(n=Count("id")).order_by("-n")
    ])

    regs = Registration.objects.filter(event__in=scoped_events(request))
    events_rows = [
        {"label": e.title_tet, "date": e.starts_at, "value": e.reg, "attended": e.att, "pk": e.pk}
        for e in scoped_events(request).annotate(
            reg=Count("registrations", filter=~Q(registrations__status="cancelled")),
            att=Count("registrations", filter=Q(registrations__status="attended")),
        ).order_by("-starts_at")[:10]
    ]
    bars(events_rows)

    year = today.year
    payments = Payment.objects.filter(member__in=members)
    rate = DuesRate.for_year(year)
    paid_year = payments.filter(year=year).aggregate(s=Sum("amount"))["s"] or Decimal("0")
    expected = (rate.annual_amount if rate else Decimal("0")) * active.count()

    return render(request, "panel/stats.html", {
        "scope": scope,
        "totals": {
            "active": active.count(), "pending": members.filter(status="pending").count(),
            "events": scoped_events(request).count(), "attended": regs.filter(status="attended").count(),
            "activities": acts.count(),
        },
        "by_muni": by_muni, "ages": ages, "growth": growth, "act_by_cat": act_by_cat, "events_rows": events_rows,
        "dues": {"year": year, "rate": rate, "paid": paid_year, "expected": expected,
                 "pct": round(100 * paid_year / expected) if expected else None},
        "generated": timezone.localtime(),
    })


@staff_member_required
def dues_report(request):
    year = int(request.GET.get("year") or date.today().year)
    rate = DuesRate.for_year(year)
    due = rate.annual_amount if rate else Decimal("0")
    members = scoped_members(request).filter(status="active").annotate(
        paid=Sum("payments__amount", filter=Q(payments__year=year))
    ).order_by("municipality__name", "full_name")
    show = request.GET.get("show", "owing")
    rows = []
    for m in members:
        paid = m.paid or Decimal("0")
        outstanding = max(Decimal("0"), due - paid)
        if show == "owing" and outstanding == 0:
            continue
        if show == "paid" and outstanding > 0:
            continue
        rows.append({"m": m, "paid": paid, "outstanding": outstanding})

    if request.method == "POST":
        from .views import scoped_members as sm
        member = sm(request).filter(pk=request.POST.get("member")).first()
        try:
            amount = Decimal((request.POST.get("amount") or "0").replace(",", "."))
        except Exception:
            amount = Decimal("0")
        if not member or amount <= 0:
            messages.error(request, "Hili membru no hatama montante.")
        else:
            Payment.objects.create(
                member=member, year=year, amount=amount, paid_on=request.POST.get("paid_on") or date.today(),
                method=request.POST.get("method") or "cash", receipt_number=request.POST.get("receipt", "")[:40],
                recorded_by=request.user,
            )
            messages.success(request, f"Pagamentu ${amount} rejista ona ba {member.full_name} ({year}).")
        return redirect(f"{request.path}?year={year}&show={show}")

    total_out = sum((r["outstanding"] for r in rows), Decimal("0"))
    return render(request, "panel/dues_report.html", {
        "year": year, "rate": rate, "rows": rows, "show": show, "total_out": total_out,
        "years": range(date.today().year, date.today().year - 6, -1), "methods": Payment.METHOD,
        "today": date.today(),
    })


def xlsx_response(filename, headers, rows, title):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill

    wb = Workbook()
    ws = wb.active
    ws.title = title[:31]
    ws.append(headers)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="C4161C")
    for r in rows:
        ws.append(r)
    for col in ws.columns:
        width = max(len(str(c.value or "")) for c in col)
        ws.column_dimensions[col[0].column_letter].width = min(45, max(10, width + 2))
    ws.freeze_panes = "A2"
    buf = BytesIO()
    wb.save(buf)
    resp = HttpResponse(buf.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp


@staff_member_required
def export_members(request):
    qs = scoped_members(request).select_related("administrative_post", "user")
    rows = [
        [m.member_number or "", m.full_name, m.get_status_display(), m.municipality.name,
         m.administrative_post.name if m.administrative_post else "", m.suco, m.aldeia, m.phone, m.user.email,
         m.birth_date, m.age, m.occupation, m.created_at.date(), m.approved_at.date() if m.approved_at else None]
        for m in qs
    ]
    headers = ["Númeru", "Naran", "Estadu", "Munisípiu", "Postu", "Suku", "Aldeia", "Telefone", "Email",
               "Data moris", "Tinan", "Servisu", "Rejista", "Aprova"]
    return xlsx_response(f"opmt-membru-{date.today()}.xlsx", headers, rows, "Membru")


@staff_member_required
def export_payments(request):
    qs = Payment.objects.filter(member__in=scoped_members(request)).select_related("member__municipality")
    rows = [[p.paid_on, p.member.member_number or "", p.member.full_name, p.member.municipality.name, p.year,
             float(p.amount), p.get_method_display(), p.receipt_number] for p in qs]
    headers = ["Data", "Númeru membru", "Naran", "Munisípiu", "Tinan kuota", "Montante (USD)", "Métodu", "Resibu"]
    return xlsx_response(f"opmt-kuota-{date.today()}.xlsx", headers, rows, "Kuota")


@staff_member_required
def export_registrations(request, event_id):
    event = scoped_events(request).filter(pk=event_id).first()
    if not event:
        return redirect("panel:list", key="events")
    rows = [[r.name, r.member.member_number if r.member else "", r.phone, r.email, r.get_status_display(),
             timezone.localtime(r.checked_in_at).strftime("%d/%m/%Y %H:%M") if r.checked_in_at else ""]
            for r in event.registrations.select_related("member")]
    return xlsx_response(f"opmt-partisipante-{event.slug}.xlsx",
                         ["Naran", "Númeru membru", "Telefone", "Email", "Estadu", "Check-in"], rows, "Partisipante")
