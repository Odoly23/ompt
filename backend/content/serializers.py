from rest_framework import serializers

from .i18n import LANGS, resolve_lang, translated_value
from .models import (
    Activity, AdministrativePost, Album, ContactMessage, Document, Figure, HistoryEvent,
    Leader, Municipality, News, Objective, Organ, Photo, Program, SecretaryGeneralMandate,
    SiteSetting,
)


class TranslatedSerializer(serializers.ModelSerializer):
    """Outputs each translated field once, in the requested language.

    Public readers get `title`, `body`… in the language chosen by ?lang= or
    Accept-Language (Tetun by default). Staff users also get and can write the
    raw columns (`title_tet`, `title_pt`, …) so the API can manage content.
    """

    translated: tuple = ()

    def get_fields(self):
        fields = super().get_fields()
        if not self._is_staff():
            for name in self.translated:
                for lang in LANGS:
                    fields.pop(f"{name}_{lang}", None)
        return fields

    def _is_staff(self):
        request = self.context.get("request")
        return bool(request and request.user and request.user.is_staff)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang = resolve_lang(self.context.get("request"))
        for name in self.translated:
            data[name] = translated_value(instance, name, lang)
        data["lang"] = lang
        return data


def make_meta(model_cls, extra_exclude=()):
    class Meta:
        model = model_cls
        exclude = tuple(extra_exclude)
    return Meta


class SiteSettingSerializer(TranslatedSerializer):
    translated = ("tagline", "about", "mission")
    Meta = make_meta(SiteSetting)


class ObjectiveSerializer(TranslatedSerializer):
    translated = ("text",)
    Meta = make_meta(Objective)


class HistoryEventSerializer(TranslatedSerializer):
    translated = ("title", "body")
    category_label = serializers.CharField(source="get_category_display", read_only=True)
    Meta = make_meta(HistoryEvent)


class FigureSerializer(TranslatedSerializer):
    translated = ("role", "bio")
    Meta = make_meta(Figure)


class MandateSerializer(TranslatedSerializer):
    translated = ("note",)
    figure_slug = serializers.CharField(source="figure.slug", read_only=True, default=None)
    Meta = make_meta(SecretaryGeneralMandate)


class LeaderSerializer(TranslatedSerializer):
    translated = ("position", "bio")
    organ_code = serializers.CharField(source="organ.code", read_only=True, default=None)
    municipality_name = serializers.CharField(source="municipality.name", read_only=True, default=None)
    Meta = make_meta(Leader)


class OrganSerializer(TranslatedSerializer):
    translated = ("name", "description")
    Meta = make_meta(Organ)


class AdministrativePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativePost
        fields = ("id", "name", "municipality", "secretary")


class MunicipalitySerializer(serializers.ModelSerializer):
    posts = AdministrativePostSerializer(many=True, read_only=True)
    activities_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Municipality
        fields = "__all__"


class ActivitySerializer(TranslatedSerializer):
    translated = ("title", "summary", "body")
    category_label = serializers.CharField(source="get_category_display", read_only=True)
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    municipality_name = serializers.CharField(source="municipality.name", read_only=True, default=None)
    Meta = make_meta(Activity)


class ProgramSerializer(TranslatedSerializer):
    translated = ("title", "description")
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    Meta = make_meta(Program)


class NewsSerializer(TranslatedSerializer):
    translated = ("title", "excerpt", "body")
    Meta = make_meta(News)


class PhotoSerializer(TranslatedSerializer):
    translated = ("caption",)
    Meta = make_meta(Photo)


class AlbumSerializer(TranslatedSerializer):
    translated = ("title",)
    photos = PhotoSerializer(many=True, read_only=True)
    photos_count = serializers.IntegerField(source="photos.count", read_only=True)
    Meta = make_meta(Album)


class DocumentSerializer(TranslatedSerializer):
    translated = ("title", "description")
    category_label = serializers.CharField(source="get_category_display", read_only=True)
    Meta = make_meta(Document)


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "phone", "subject", "message")

    def validate(self, attrs):
        if not attrs.get("email") and not attrs.get("phone"):
            raise serializers.ValidationError("Hatama email ka telefone atu ami bele hatán.")
        return attrs
