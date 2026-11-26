"""Helpers for content stored in four languages (Tetun, Portuguese, Indonesian, English).

Each translated field is stored as four columns: <name>_tet, <name>_pt, <name>_id, <name>_en.
Tetun is required; the others fall back to Tetun when empty.
"""
from django.conf import settings
from django.db import models

LANGS = settings.SITE_LANGUAGES  # ["tet", "pt", "id", "en"]
LANG_LABELS = {"tet": "Tetun", "pt": "Português", "id": "Indonesia", "en": "English"}


def tr_char(max_length=255, required=True):
    """Return a dict of four CharFields to splat into a model with `locals().update`."""
    return {
        lang: models.CharField(max_length=max_length, blank=not (required and lang == "tet"))
        for lang in LANGS
    }


def tr_text(required=False):
    return {lang: models.TextField(blank=not (required and lang == "tet")) for lang in LANGS}


def add_translated(cls_attrs, name, kind="char", **kwargs):
    fields = tr_char(**kwargs) if kind == "char" else tr_text(**kwargs)
    for lang, field in fields.items():
        cls_attrs[f"{name}_{lang}"] = field


def resolve_lang(request):
    """Pick the language from ?lang=, then Accept-Language, then the default (Tetun)."""
    if request is None:
        return settings.DEFAULT_SITE_LANGUAGE
    lang = request.query_params.get("lang") if hasattr(request, "query_params") else None
    if lang in LANGS:
        return lang
    header = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
    for part in header.split(","):
        code = part.split(";")[0].strip().lower()
        if code.startswith("tet"):
            return "tet"
        base = code.split("-")[0]
        if base in LANGS:
            return base
    return settings.DEFAULT_SITE_LANGUAGE


def translated_value(obj, name, lang):
    value = getattr(obj, f"{name}_{lang}", "") or ""
    if not value:
        value = getattr(obj, f"{name}_tet", "") or ""
    return value


class TranslatedMixin:
    """Model mixin: obj.t("title", "pt")."""

    def t(self, name, lang="tet"):
        return translated_value(self, name, lang)
