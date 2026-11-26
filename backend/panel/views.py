from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.models import MemberProfile
from content.i18n import LANG_LABELS, LANGS
from content.models import Activity, ContactMessage, News, SiteSetting

from .registry import EXCLUDE_FIELDS, REGISTRY


staff_member_required = user_passes_test(lambda u: u.is_active and u.is_staff, login_url="panel:login")


class LoginView(auth_views.LoginView):
    template_name = "panel/login.html"
    redirect_authenticated_user = True


def get_entry(key):
    if key not in REGISTRY:
        raise Http404
    return REGISTRY[key]


def split_fields(form):
    """Separate the form's fields into plain fields and per-language tabs."""
    plain, by_lang = [], {lang: [] for lang in LANGS}
    for bound in form:
        name = bound.name
        suffix = name.rsplit("_", 1)[-1] if "_" in name else ""
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
    return value if value not in (None, "") else "–"


@staff_member_required
def dashboard(request):
    ctx = {
        "counts": {
            "members_pending": MemberProfile.objects.filter(status="pending").count(),
            "members_active": MemberProfile.objects.filter(status="active").count(),
            "activities": Activity.objects.count(),
            "news": News.objects.count(),
            "messages_unread": ContactMessage.objects.filter(is_read=False).count(),
        },
        "pending": MemberProfile.objects.filter(status="pending").select_related("municipality")[:8],
        "latest_messages": ContactMessage.objects.all()[:5],
        "sample_counts": sample_counts(),
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


@staff_member_required
def object_list(request, key):
    model, group, columns, search = get_entry(key)
    qs = model.objects.all()
    q = request.GET.get("q", "").strip()
    if q:
        cond = Q()
        for f in search:
            cond |= Q(**{f"{f}__icontains": q})
        qs = qs.filter(cond)
    status = request.GET.get("status")
    if key == "members" and status:
        qs = qs.filter(status=status)
    if request.GET.get("sample") == "1" and any(f.name == "is_sample" for f in model._meta.fields):
        qs = qs.filter(is_sample=True)
    page = Paginator(qs, 25).get_page(request.GET.get("page"))
    headers = [model._meta.get_field(c).verbose_name for c in columns]
    rows = [(obj, [cell(obj, c) for c in columns]) for obj in page]
    return render(request, "panel/list.html", {
        "key": key, "model_name": model._meta.verbose_name_plural, "headers": headers,
        "rows": rows, "page": page, "q": q, "group": group,
        "has_sample": any(f.name == "is_sample" for f in model._meta.fields),
    })


@staff_member_required
def object_edit(request, key, pk=None):
    model, group, *_r = get_entry(key)
    obj = get_object_or_404(model, pk=pk) if pk else None
    exclude = [f for f in EXCLUDE_FIELDS if any(x.name == f for x in model._meta.fields)]
    Form = modelform_factory(model, exclude=exclude)
    form = Form(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        saved = form.save()
        messages.success(request, f"Rai ona: {saved}")
        if "save_add" in request.POST:
            return redirect("panel:add", key=key)
        return redirect("panel:list", key=key)
    plain, tabs = split_fields(form)
    return render(request, "panel/form.html", {
        "key": key, "obj": obj, "form": form, "plain": plain, "tabs": tabs,
        "model_name": model._meta.verbose_name, "group": group,
    })


@staff_member_required
def object_delete(request, key, pk):
    model, *_r = get_entry(key)
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        label = str(obj)
        obj.delete()
        messages.success(request, f"Hamoos ona: {label}")
        return redirect("panel:list", key=key)
    return render(request, "panel/confirm_delete.html", {"obj": obj, "key": key})


@staff_member_required
@require_POST
def member_status(request, pk, action):
    member = get_object_or_404(MemberProfile, pk=pk)
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


@staff_member_required
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
