from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from content.views import IsStaffOrReadOnly, is_staff

from .models import Story

MAX_PHOTO = 8 * 1024 * 1024
MAX_AUDIO = 25 * 1024 * 1024


class StorySerializer(serializers.ModelSerializer):
    municipality_name = serializers.CharField(source="municipality.name", read_only=True, default=None)
    era_label = serializers.CharField(source="get_era_display", read_only=True)
    front_label = serializers.CharField(source="get_front_display", read_only=True)

    class Meta:
        model = Story
        exclude = ("submitted_by", "submitter_contact", "moderation_note", "consent")


class StorySubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ("title", "storyteller", "nickname", "municipality", "era", "front", "language", "summary",
                  "body", "photo", "audio", "video_url", "submitted_by", "submitter_contact", "consent")
        extra_kwargs = {"submitted_by": {"required": True}, "submitter_contact": {"required": True}}

    def validate_consent(self, value):
        if not value:
            raise serializers.ValidationError("Presiza lisensa husi na'in ba istória (ka família) atu publika.")
        return value

    def validate_photo(self, f):
        if f and f.size > MAX_PHOTO:
            raise serializers.ValidationError("Foto boot liu (maksimu 8 MB).")
        return f

    def validate_audio(self, f):
        if not f:
            return f
        if f.size > MAX_AUDIO:
            raise serializers.ValidationError("Áudiu boot liu (maksimu 25 MB).")
        if not f.name.lower().endswith((".mp3", ".m4a", ".ogg", ".wav", ".aac")):
            raise serializers.ValidationError("Formatu áudiu: mp3, m4a, ogg, wav ka aac.")
        return f

    def validate_body(self, value):
        if len(value.strip()) < 80:
            raise serializers.ValidationError("Istória badak liu. Hakerek pelumenus liafuan 80 karakter.")
        return value


class StoryViewSet(viewsets.ModelViewSet):
    def get_throttles(self):
        if self.action == "submit":
            self.throttle_scope = "story"
            return [ScopedRateThrottle()]
        return super().get_throttles()

    serializer_class = StorySerializer
    permission_classes = [IsStaffOrReadOnly]
    lookup_field = "slug"
    filterset_fields = ["era", "front", "municipality__code", "language", "is_featured"]
    search_fields = ["title", "storyteller", "nickname", "summary", "body"]

    def get_queryset(self):
        qs = Story.objects.select_related("municipality")
        return qs if is_staff(self.request) else qs.filter(status="published")

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny],
            parser_classes=[MultiPartParser, FormParser, JSONParser])
    def submit(self, request):
        s = StorySubmitSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        s.save(status="pending")
        return Response({"detail": "ok"}, status=201)

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def choices(self, request):
        return Response({
            "era": [{"value": v, "label": l} for v, l in Story.ERA],
            "front": [{"value": v, "label": l} for v, l in Story.FRONT],
            "language": [{"value": v, "label": l} for v, l in Story.LANG],
        })
