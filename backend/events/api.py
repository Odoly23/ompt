from datetime import timedelta
from datetime import timezone as dt_tz

from django.db import IntegrityError
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from content.serializers import TranslatedSerializer, make_meta
from content.views import BaseViewSet

from .models import Event, Registration


def member_of(request):
    user = request.user
    return getattr(user, "member", None) if user.is_authenticated else None


class EventSerializer(TranslatedSerializer):
    translated = ("title", "description")
    municipality_name = serializers.CharField(source="municipality.name", read_only=True, default=None)
    registered_count = serializers.IntegerField(read_only=True)
    spots_left = serializers.IntegerField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    my_registration = serializers.SerializerMethodField()
    Meta = make_meta(Event)

    def get_my_registration(self, obj):
        member = member_of(self.context.get("request"))
        if not member:
            return None
        reg = obj.registrations.filter(member=member).exclude(status="cancelled").first()
        return {"id": reg.id, "status": reg.status} if reg else None


class RegistrationInSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=60, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)


class MyRegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.SerializerMethodField()
    event_slug = serializers.CharField(source="event.slug")
    starts_at = serializers.DateTimeField(source="event.starts_at")
    time_confirmed = serializers.BooleanField(source="event.time_confirmed")
    location = serializers.CharField(source="event.location")

    class Meta:
        model = Registration
        fields = ("id", "status", "checked_in_at", "event_title", "event_slug", "starts_at", "time_confirmed", "location")

    def get_event_title(self, obj):
        from content.i18n import resolve_lang
        return obj.event.t("title", resolve_lang(self.context.get("request")))


def ics_escape(text):
    return (text or "").replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


class EventViewSet(BaseViewSet):
    def get_throttles(self):
        if self.action == "register":
            self.throttle_scope = "event_register"
            return [ScopedRateThrottle()]
        return super().get_throttles()

    queryset = Event.objects.select_related("municipality")
    serializer_class = EventSerializer
    published_field = "is_published"
    lookup_field = "slug"
    filterset_fields = ["municipality__code"]
    search_fields = ["title_tet", "title_pt", "title_id", "title_en", "location"]

    def get_queryset(self):
        qs = super().get_queryset()
        when = self.request.query_params.get("when")
        now = timezone.now()
        if when == "upcoming":
            qs = qs.filter(starts_at__gte=now - timedelta(hours=12))
        elif when == "past":
            qs = qs.filter(starts_at__lt=now - timedelta(hours=12)).order_by("-starts_at")
        return qs

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def register(self, request, slug=None):
        event = self.get_object()
        if event.is_past or not event.registration_open:
            return Response({"detail": "Rejistu taka ona ba eventu ne'e."}, status=400)
        if event.spots_left == 0:
            return Response({"detail": "Fatin nakonu ona."}, status=400)
        member = member_of(request)
        if event.members_only and not (member and member.status == "active"):
            return Response({"detail": "Eventu ne'e ba membru ativu deit. Halo login uluk."}, status=403)

        data = RegistrationInSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        if member:
            reg, created = Registration.objects.get_or_create(
                event=event, member=member,
                defaults={"name": member.full_name, "phone": member.phone, "email": request.user.email},
            )
            if not created and reg.status == "cancelled":
                reg.status = "registered"
                reg.save(update_fields=["status"])
        else:
            v = data.validated_data
            if not v.get("name") or not (v.get("phone") or v.get("email")):
                return Response({"detail": "Hatama naran no telefone ka email."}, status=400)
            if Registration.objects.filter(event=event, member__isnull=True, phone=v.get("phone", ""), email=v.get("email", ""), name=v["name"]).exists():
                return Response({"detail": "Ita rejista tiha ona."}, status=400)
            try:
                reg = Registration.objects.create(event=event, **v)
            except IntegrityError:
                return Response({"detail": "Ita rejista tiha ona."}, status=400)
        return Response({"id": reg.id, "status": reg.status, "registered_count": event.registered_count}, status=201)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, slug=None):
        member = member_of(request)
        reg = Registration.objects.filter(event__slug=slug, member=member).first() if member else None
        if not reg:
            return Response({"detail": "Rejistu la iha."}, status=404)
        reg.status = "cancelled"
        reg.save(update_fields=["status"])
        return Response(status=204)

    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def ics(self, request, slug=None):
        """Add-to-calendar file (.ics)."""
        e = self.get_object()
        fmt = "%Y%m%dT%H%M%SZ"
        start = e.starts_at.astimezone(dt_tz.utc)
        end = (e.ends_at or e.starts_at + timedelta(hours=2)).astimezone(dt_tz.utc)
        body = "\r\n".join([
            "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//OPMT//Agenda//TET",
            "BEGIN:VEVENT",
            f"UID:opmt-event-{e.pk}@opmt",
            f"DTSTAMP:{timezone.now().astimezone(dt_tz.utc).strftime(fmt)}",
            f"DTSTART:{start.strftime(fmt)}",
            f"DTEND:{end.strftime(fmt)}",
            f"SUMMARY:{ics_escape(e.title_tet)}",
            f"LOCATION:{ics_escape(e.location)}",
            f"DESCRIPTION:{ics_escape(e.description_tet)}",
            "END:VEVENT", "END:VCALENDAR", "",
        ])
        resp = HttpResponse(body, content_type="text/calendar; charset=utf-8")
        resp["Content-Disposition"] = f'attachment; filename="opmt-{e.slug}.ics"'
        return resp
