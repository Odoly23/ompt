import json
from datetime import date

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import modelform_factory
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.models import MemberProfile, StaffProfile
from archive.models import Story
from comms.models import Announcement
from comms.senders import send_announcement
from content.i18n import LANG_LABELS, LANGS
from content.models import Activity, ContactMessage, Municipality, News, SiteSetting
from dues.models import DuesRate, Payment
from events.models import Event, Registration

from .registry import EXCLUDE_FIELDS, REGISTRY, SCOPE, allowed_keys, user_scope

staff_member_required = user_passes_test(lambda u: u.is_active and u.is_staff, login_url="panel:login")


def national_only(view):
    def wrapper(request, *args, **kwargs):
        if user_scope(request.user) is not None:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return staff_member_required(wrapper)


class LoginView(auth_views.LoginView):
    template_name = "panel/login.html"
    redirect_authenticated_user = True


# ---------- scoping helpers ----------

def get_entry(request, key):
    if key not in REGISTRY or key not in allowed_keys(request.user):
        raise Http404
    return REGISTRY[key]


def scoped(request, key, qs):
    scope = user_scope(request.user)
    if scope is None:
        return qs
    return qs.filter(**{SCOPE[key]: scope})


def scoped_members(request):
    qs = MemberProfile.objects.select_related("municipality")
    scope = user_scope(request.user)
    return qs if scope is None else qs.filter(municipality=scope)


def scoped_events(request):
    qs = Event.objects.all()
    scope = user_scope(request.user)
    return qs if scope is None else qs.filter(Q(municipality=scope) | Q(municipality__isnull=True))


def limit_form(request, form):
    """Coordinators can only pick their own municipality, members and events."""
    scope = user_scope(request.user)
    if scope is None:
        return form
    for name, field in form.fields.items():
        model = getattr(getattr(field, "queryset", None), "model", None)
        if model is Municipality:
            field.queryset = Municipality.objects.filter(pk=scope.pk)
            field.required = True
            field.initial = scope.pk
            field.empty_label = None
        elif model is MemberProfile:
            field.queryset = MemberProfile.objects.filter(municipality=scope)
        elif model is Event:
            field.queryset = scoped_events(request)
    return form


def split_fields(form):
    """Separate the form's fields into plain fields and per-language tabs."""
    plain, by_lang = [], {lang: [] for lang in LANGS}
    for bound in form:
        suffix = bound.name.rsplit("_", 1)[-1] if "_" in bound.name else ""
        if suffix in LANGS:
            by_lang[suffix].append(bound)
        else:
            plain.append(bound)
    tabs = [(lang, LANG_LABELS[lang], fields) for lang, fields in by_lang.items() if fields]
    return plain, tabs


def cell(obj, field):
    value = getattr(obj, field)
    display = getattr(obj, f"get_{field}_display", None)
    if display:
        return display()
    if isinstance(value, bool):
        return "✓" if value else "–"
    if hasattr(value, "strftime"):
        return value.strftime("%d/%m/%Y %H:%M") if hasattr(value, "hour") else value.strftime("%d/%m/%Y")
    return value if value not in (None, "") else "–"


# ---------- dashboard ----------

@staff_member_required
def dashboard(request):
    members = scoped_members(request)
    scope = user_scope(request.user)
    ctx = {
        "counts": {
            "members_pending": members.filter(status="pending").count(),
            "members_active": members.filter(status="active").count(),
            "activities": Activity.objects.filter(**({"municipality": scope} if scope else {})).count(),
            "events_upcoming": scoped_events(request).filter(starts_at__gte=timezone.now()).count(),
            "stories_pending": scoped(request, "stories", Story.objects.filter(status="pending")).count(),
            "news": News.objects.count(),
            "messages_unread": ContactMessage.objects.filter(is_read=False).count() if scope is None else None,
        },
        "pending": members.filter(status="pending")[:8],
        "latest_messages": ContactMessage.objects.all()[:5] if scope is None else [],
        "next_events": scoped_events(request).filter(starts_at__gte=timezone.now())[:5],
        "sample_counts": sample_counts() if scope is None else [],
    }
    return render(request, "panel/dashboard.html", ctx)


def sample_counts():
    out = []
    for key, (model, *_r) in REGISTRY.items():
        if any(f.name == "is_sample" for f in model._meta.fields):
            n = model.objects.filter(is_sample=True).count()
            if n:
                out.append((key, model._meta.verbose_name_plural, n))
    return out


# ---------- generic CRUD ----------

@staff_member_required
def object_list(request, key):
    model, group, columns, search = get_entry(request, key)
    qs = scoped(request, key, model.objects.all())
    q = request.GET.get("q", "").strip()
    if q:
        cond = Q()
        for f in search:
            cond |= Q(**{f"{f}__icontains": q})
        qs = qs.filter(cond)
    status = request.GET.get("status")
    if status and any(f.name == "status" for f in model._meta.fields):
        qs = qs.filter(status=status)
    if request.GET.get("sample") == "1" and any(f.name == "is_sample" for f in model._meta.fields):
        qs = qs.filter(is_sample=True)
    event_id = request.GET.get("event")
    if key == "registrations" and event_id:
        qs = qs.filter(event_id=event_id)
    status_field = next((f for f in model._meta.fields if f.name == "status"), None)
    page = Paginator(qs, 25).get_page(request.GET.get("page"))
    headers = [model._meta.get_field(c).verbose_name for c in columns]
    rows = [(obj, [cell(obj, c) for c in columns]) for obj in page]
    return render(request, "panel/list.html", {
        "key": key, "model_name": model._meta.verbose_name_plural, "headers": headers,
        "rows": rows, "page": page, "q": q, "group": group,
        "status_choices": status_field.choices if status_field else None,
        "has_sample": any(f.name == "is_sample" for f in model._meta.fields),
        "export_url": {"members": "panel:export_members", "payments": "panel:export_payments"}.get(key),
    })


@staff_member_required
def object_edit(request, key, pk=None):
    model, group, *_r = get_entry(request, key)
    obj = get_object_or_404(scoped(request, key, model.objects.all()), pk=pk) if pk else None
    if key == "announcements" and obj and obj.status == "sent":
        messages.info(request, "Anúnsiu ne'e haruka tiha ona; la bele edita.")
        return redirect("panel:list", key=key)
    exclude = [f for f in EXCLUDE_FIELDS if any(x.name == f for x in model._meta.fields)]
    if key == "announcements":
        exclude.append("status")
    Form = modelform_factory(model, exclude=exclude)
    form = limit_form(request, Form(request.POST or None, request.FILES or None, instance=obj))
    if request.method == "POST" and form.is_valid():
        saved = form.save(commit=False)
        if key == "payments" and not saved.recorded_by_id:
            saved.recorded_by = request.user
        saved.save()
        form.save_m2m()
        messages.success(request, f"Rai ona: {saved}")
        if "save_add" in request.POST:
            return redirect("panel:add", key=key)
        if key == "announcements":
            return redirect("panel:announcement_send", pk=saved.pk)
        return redirect("panel:list", key=key)
    if key == "messages" and obj and not obj.is_read:
        obj.is_read = True
        obj.save(update_fields=["is_read"])
    plain, tabs = split_fields(form)
    return render(request, "panel/form.html", {
        "key": key, "obj": obj, "form": form, "plain": plain, "tabs": tabs,
        "model_name": model._meta.verbose_name, "group": group,
    })


@staff_member_required
def object_delete(request, key, pk):
    model, *_r = get_entry(request, key)
    obj = get_object_or_404(scoped(request, key, model.objects.all()), pk=pk)
    if request.method == "POST":
        label = str(obj)
        obj.delete()
        messages.success(request, f"Hamoos ona: {label}")
        return redirect("panel:list", key=key)
    return render(request, "panel/confirm_delete.html", {"obj": obj, "key": key})


@staff_member_required
@require_POST
def member_status(request, pk, action):
    member = get_object_or_404(scoped_members(request), pk=pk)
    if action == "approve":
        member.status = "active"
        member.approved_at = timezone.now()
        member.assign_number()
        messages.success(request, f"{member.full_name} aprova ona ({member.member_number}).")
    elif action == "reject":
        member.status = "rejected"
        member.status_note = request.POST.get("note", "")[:255]
        messages.warning(request, f"{member.full_name} rejeita ona.")
    else:
        raise Http404
    member.save()
    next_url = request.POST.get("next", "")
    if next_url.startswith("/panel/"):
        return redirect(next_url)
    return redirect("panel:list", key="members")


@national_only
def site_settings(request):
    setting = SiteSetting.load()
    Form = modelform_factory(SiteSetting, exclude=("created_at", "updated_at"))
    form = Form(request.POST or None, request.FILES or None, instance=setting)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Konfigurasaun rai ona.")
        return redirect("panel:settings")
    plain, tabs = split_fields(form)
    return render(request, "panel/form.html", {
        "form": form, "plain": plain, "tabs": tabs, "model_name": "Konfigurasaun website",
        "obj": setting, "is_settings": True,
    })


# ---------- QR scan: card check & event check-in ----------

@staff_member_required
def scan(request):
    events = scoped_events(request).filter(starts_at__date__gte=date.today().replace(day=1)).order_by("starts_at")
    return render(request, "panel/scan.html", {"events": events, "selected": request.GET.get("event", "")})


@staff_member_required
@require_POST
def scan_check(request):
    """Body: {"code": "<qr text or token>", "event": <id or null>} → member info, and check-in if an event is given."""
    try:
        payload = json.loads(request.body or "{}")
    except ValueError:
        return JsonResponse({"ok": False, "error": "Dadus la válidu."}, status=400)
    code = (payload.get("code") or "").strip().rstrip("/")
    token = code.rsplit("/", 1)[-1]
    member = MemberProfile.objects.select_related("municipality").filter(card_token=token).first() if len(token) == 36 else None
    if member is None and code:
        member = MemberProfile.objects.select_related("municipality").filter(member_number__iexact=code).first()
    if member is None:
        return JsonResponse({"ok": False, "error": "Kartaun la rekoñese."}, status=404)

    from dues.models import member_balance
    _, _, outstanding = member_balance(member, date.today().year)
    info = {
        "full_name": member.full_name, "member_number": member.member_number, "status": member.get_status_display(),
        "active": member.status == "active", "municipality": member.municipality.name,
        "photo": member.photo.url if member.photo else None, "dues_outstanding": str(outstanding),
    }
    event_id = payload.get("event")
    if event_id:
        event = get_object_or_404(scoped_events(request), pk=event_id)
        reg, created = Registration.objects.get_or_create(
            event=event, member=member,
            defaults={"name": member.full_name, "phone": member.phone, "email": member.user.email},
        )
        already = reg.status == "attended"
        if not already:
            reg.check_in(request.user)
        info["checkin"] = {"event": event.title_tet, "already": already, "walk_in": created,
                           "time": timezone.localtime(reg.checked_in_at).strftime("%H:%M")}
    return JsonResponse({"ok": True, "member": info})


@staff_member_required
@require_POST
def registration_checkin(request, pk):
    reg = get_object_or_404(scoped(request, "registrations", Registration.objects.all()), pk=pk)
    reg.check_in(request.user)
    messages.success(request, f"{reg.name}: check-in ona.")
    next_url = request.POST.get("next", "")
    if next_url.startswith("/panel/"):
        return redirect(next_url)
    return redirect("panel:list", key="registrations")


# ---------- announcements ----------

@staff_member_required
def announcement_send(request, pk):
    ann = get_object_or_404(scoped(request, "announcements", Announcement.objects.all()), pk=pk)
    recipients = ann.recipients()
    if user_scope(request.user) is not None and ann.municipality_id != user_scope(request.user).pk:
        raise PermissionDenied
    if request.method == "POST":
        if ann.status == "sent":
            messages.info(request, "Anúnsiu ne'e haruka tiha ona.")
        else:
            send_announcement(ann, request.user)
            messages.success(request, f"Haruka ona ba membru {ann.recipients_count}: email {ann.email_sent}, SMS {ann.sms_sent}, falla {ann.failures}.")
        return redirect("panel:list", key="announcements")
    return render(request, "panel/announcement_send.html", {
        "ann": ann,
        "count": recipients.count(),
        "with_email": recipients.exclude(user__email="").count(),
        "with_phone": recipients.exclude(phone="").count(),
    })


# ---------- team (national only) ----------

@national_only
def team(request):
    User = get_user_model()
    error = None
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        name = request.POST.get("name", "").strip()
        password = request.POST.get("password", "")
        muni_id = request.POST.get("municipality") or None
        role = request.POST.get("role", "").strip()
        if not email or not name or len(password) < 8:
            error = "Hatama naran, email no password (karakter 8 ka liu)."
        elif User.objects.filter(username=email).exists():
            error = "Email ne'e iha ona konta."
        else:
            first, _, last = name.partition(" ")
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first, last_name=last, is_staff=True)
            StaffProfile.objects.create(user=user, municipality_id=muni_id, role=role)
            messages.success(request, f"Konta ekipa kria ona ba {name}.")
            return redirect("panel:team")
    staff = User.objects.filter(is_staff=True).select_related("staff_profile__municipality").order_by("staff_profile__municipality__name", "first_name")
    return render(request, "panel/team.html", {"staff": staff, "municipalities": Municipality.objects.all(), "error": error})


@national_only
@require_POST
def team_toggle(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk, is_superuser=False)
    user.is_active = not user.is_active
    user.save(update_fields=["is_active"])
    messages.success(request, f"{user.get_full_name() or user.username}: {'ativu' if user.is_active else 'la ativu'}.")
    return redirect("panel:team")
