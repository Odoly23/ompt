"""Which models the Bootstrap 4 panel manages, and how they are listed."""
from accounts.models import MemberProfile
from content.models import (
    Activity, AdministrativePost, Album, ContactMessage, Document, Figure, HistoryEvent, Leader,
    Municipality, News, Objective, Organ, Photo, Program, SecretaryGeneralMandate, Slide,
)

# key: (model, menu group, list columns, search fields)
REGISTRY = {
    "history": (HistoryEvent, "Istória", ["year", "title_tet", "category", "is_published", "is_sample"], ["title_tet"]),
    "figures": (Figure, "Istória", ["name", "nickname", "role_tet", "is_heroine"], ["name", "nickname"]),
    "mandates": (SecretaryGeneralMandate, "Istória", ["number", "name", "start_year", "end_year"], ["name"]),
    "objectives": (Objective, "Istória", ["kind", "order", "text_tet"], ["text_tet"]),
    "organs": (Organ, "Lideransa", ["order", "name_tet", "code"], ["name_tet"]),
    "leaders": (Leader, "Lideransa", ["name", "position_tet", "organ", "municipality", "is_active", "is_sample"], ["name"]),
    "municipalities": (Municipality, "Lideransa", ["name", "coordinator", "members_count", "sucos_with_structure", "is_sample"], ["name", "coordinator"]),
    "posts": (AdministrativePost, "Lideransa", ["name", "municipality", "secretary"], ["name"]),
    "activities": (Activity, "Atividade", ["date", "title_tet", "category", "status", "municipality", "is_published"], ["title_tet", "location"]),
    "programs": (Program, "Atividade", ["order", "title_tet", "status"], ["title_tet"]),
    "slides": (Slide, "Komunikasaun", ["order", "title_tet", "theme", "is_active"], ["title_tet"]),
    "news": (News, "Komunikasaun", ["published_at", "title_tet", "is_published", "is_sample"], ["title_tet"]),
    "albums": (Album, "Komunikasaun", ["date", "title_tet", "activity"], ["title_tet"]),
    "photos": (Photo, "Komunikasaun", ["album", "caption_tet", "order"], ["caption_tet"]),
    "documents": (Document, "Komunikasaun", ["year", "title_tet", "category", "is_public"], ["title_tet"]),
    "messages": (ContactMessage, "Komunikasaun", ["created_at", "name", "subject", "is_read"], ["name", "subject", "email"]),
    "members": (MemberProfile, "Membru", ["member_number", "full_name", "municipality", "phone", "status", "created_at"], ["full_name", "phone", "member_number", "user__email"]),
}

EXCLUDE_FIELDS = ("created_at", "updated_at", "slug", "user", "approved_at", "member_number")


def menu():
    groups = {}
    for key, (model, group, *_rest) in REGISTRY.items():
        groups.setdefault(group, []).append((key, model._meta.verbose_name_plural))
    return groups
