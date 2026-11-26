"""Which models the Bootstrap 4 panel manages, how they are listed, and how
municipal coordinators are scoped to their own municipality."""
from accounts.models import MemberProfile
from archive.models import Story
from comms.models import Announcement
from content.models import (
    Activity, AdministrativePost, Album, ContactMessage, Document, Figure, HistoryEvent, Leader,
    Municipality, News, Objective, Organ, Photo, Program, SecretaryGeneralMandate, Slide,
)
from dues.models import DuesRate, Payment
from events.models import Event, Registration

# key: (model, menu group, list columns, search fields)
REGISTRY = {
    "history": (HistoryEvent, "Istória", ["year", "title_tet", "category", "is_published", "is_sample"], ["title_tet"]),
    "figures": (Figure, "Istória", ["name", "nickname", "role_tet", "is_heroine"], ["name", "nickname"]),
    "mandates": (SecretaryGeneralMandate, "Istória", ["number", "name", "start_year", "end_year"], ["name"]),
    "objectives": (Objective, "Istória", ["kind", "order", "text_tet"], ["text_tet"]),
    "stories": (Story, "Istória", ["created_at", "title", "storyteller", "municipality", "status", "is_featured"], ["title", "storyteller", "body"]),
    "organs": (Organ, "Lideransa", ["order", "name_tet", "code"], ["name_tet"]),
    "leaders": (Leader, "Lideransa", ["name", "position_tet", "organ", "municipality", "is_active", "is_sample"], ["name"]),
    "municipalities": (Municipality, "Lideransa", ["name", "coordinator", "members_count", "sucos_with_structure", "is_sample"], ["name", "coordinator"]),
    "posts": (AdministrativePost, "Lideransa", ["name", "municipality", "secretary"], ["name"]),
    "activities": (Activity, "Atividade", ["date", "title_tet", "category", "status", "municipality", "is_published"], ["title_tet", "location"]),
    "events": (Event, "Atividade", ["starts_at", "title_tet", "municipality", "capacity", "registration_open", "is_published", "is_sample"], ["title_tet", "location"]),
    "registrations": (Registration, "Atividade", ["created_at", "name", "event", "phone", "status", "checked_in_at"], ["name", "phone", "email"]),
    "programs": (Program, "Atividade", ["order", "title_tet", "status"], ["title_tet"]),
    "slides": (Slide, "Komunikasaun", ["order", "title_tet", "theme", "is_active"], ["title_tet"]),
    "news": (News, "Komunikasaun", ["published_at", "title_tet", "is_published", "is_sample"], ["title_tet"]),
    "albums": (Album, "Komunikasaun", ["date", "title_tet", "activity"], ["title_tet"]),
    "photos": (Photo, "Komunikasaun", ["album", "caption_tet", "order"], ["caption_tet"]),
    "documents": (Document, "Komunikasaun", ["year", "title_tet", "category", "is_public"], ["title_tet"]),
    "announcements": (Announcement, "Komunikasaun", ["created_at", "title", "channel", "municipality", "status", "recipients_count"], ["title", "body"]),
    "messages": (ContactMessage, "Komunikasaun", ["created_at", "name", "subject", "is_read"], ["name", "subject", "email"]),
    "members": (MemberProfile, "Membru", ["member_number", "full_name", "municipality", "phone", "status", "created_at"], ["full_name", "phone", "member_number", "user__email"]),
    "payments": (Payment, "Membru", ["paid_on", "member", "year", "amount", "method", "receipt_number"], ["member__full_name", "member__member_number", "receipt_number"]),
    "rates": (DuesRate, "Membru", ["year", "annual_amount", "note"], ["note"]),
}

# For municipal coordinators: the lookup that ties a row to a municipality.
# Keys not listed here are for national staff only.
SCOPE = {
    "members": "municipality",
    "activities": "municipality",
    "events": "municipality",
    "registrations": "event__municipality",
    "payments": "member__municipality",
    "stories": "municipality",
    "announcements": "municipality",
    "posts": "municipality",
}

EXCLUDE_FIELDS = ("created_at", "updated_at", "slug", "user", "approved_at", "member_number",
                  "card_token", "recorded_by", "sent_at", "sent_by", "recipients_count", "email_sent",
                  "sms_sent", "failures", "checked_in_by")

# Extra pages shown in the menu: (url name, label, group, national only)
EXTRA_PAGES = [
    ("panel:stats", "Estatístika", "Dashboard", False),
    ("panel:scan", "Scan QR / check-in", "Dashboard", False),
    ("panel:dues_report", "Relatóriu kuota", "Membru", False),
    ("panel:team", "Ekipa panel", "Sistema", True),
]


def user_scope(user):
    """None for national staff, else the coordinator's Municipality."""
    if user.is_superuser:
        return None
    profile = getattr(user, "staff_profile", None)
    return profile.municipality if profile else None


def allowed_keys(user):
    scope = user_scope(user)
    return list(REGISTRY) if scope is None else [k for k in REGISTRY if k in SCOPE]


def menu(user):
    keys = allowed_keys(user)
    national = user_scope(user) is None
    groups = {}
    for key in keys:
        model, group, *_ = REGISTRY[key]
        groups.setdefault(group, []).append(("list", key, model._meta.verbose_name_plural))
    for url, label, group, national_only in EXTRA_PAGES:
        if national_only and not national:
            continue
        groups.setdefault(group, []).insert(0, ("page", url, label))
    order = ["Dashboard", "Membru", "Atividade", "Istória", "Lideransa", "Komunikasaun", "Sistema"]
    return {g: groups[g] for g in order if g in groups}
