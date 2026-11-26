from django.db.models import Count, Q, Sum
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from .models import (
    Activity, Album, Document, Figure, HistoryEvent, Leader, Municipality, News, Objective,
    Organ, Program, SecretaryGeneralMandate, SiteSetting,
)
from . import serializers as s


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


def is_staff(request):
    return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    published_field = None

    def get_queryset(self):
        qs = super().get_queryset()
        if self.published_field and not is_staff(self.request):
            qs = qs.filter(**{self.published_field: True})
        return qs


class ObjectiveViewSet(BaseViewSet):
    queryset = Objective.objects.all()
    serializer_class = s.ObjectiveSerializer
    pagination_class = None
    filterset_fields = ["kind"]


class HistoryEventViewSet(BaseViewSet):
    queryset = HistoryEvent.objects.all()
    serializer_class = s.HistoryEventSerializer
    published_field = "is_published"
    pagination_class = None
    filterset_fields = ["category", "year"]


class FigureViewSet(BaseViewSet):
    queryset = Figure.objects.all()
    serializer_class = s.FigureSerializer
    lookup_field = "slug"
    pagination_class = None
    filterset_fields = ["is_heroine"]


class MandateViewSet(BaseViewSet):
    queryset = SecretaryGeneralMandate.objects.select_related("figure")
    serializer_class = s.MandateSerializer
    pagination_class = None


class OrganViewSet(BaseViewSet):
    queryset = Organ.objects.all()
    serializer_class = s.OrganSerializer
    lookup_field = "code"
    pagination_class = None


class LeaderViewSet(BaseViewSet):
    queryset = Leader.objects.select_related("organ", "municipality")
    serializer_class = s.LeaderSerializer
    published_field = "is_active"
    pagination_class = None
    filterset_fields = ["organ__code", "municipality"]


class MunicipalityViewSet(BaseViewSet):
    queryset = Municipality.objects.prefetch_related("posts").annotate(
        activities_count=Count("activity", filter=Q(activity__is_published=True))
    )
    serializer_class = s.MunicipalitySerializer
    lookup_field = "code"
    pagination_class = None


class ActivityViewSet(BaseViewSet):
    queryset = Activity.objects.select_related("municipality")
    serializer_class = s.ActivitySerializer
    published_field = "is_published"
    lookup_field = "slug"
    filterset_fields = ["category", "status", "municipality__code"]
    search_fields = ["title_tet", "title_pt", "title_id", "title_en", "location"]
    ordering_fields = ["date", "created_at"]


class ProgramViewSet(BaseViewSet):
    queryset = Program.objects.all()
    serializer_class = s.ProgramSerializer
    pagination_class = None


class NewsViewSet(BaseViewSet):
    queryset = News.objects.all()
    serializer_class = s.NewsSerializer
    published_field = "is_published"
    lookup_field = "slug"
    search_fields = ["title_tet", "title_pt", "title_id", "title_en"]


class AlbumViewSet(BaseViewSet):
    queryset = Album.objects.prefetch_related("photos")
    serializer_class = s.AlbumSerializer
    lookup_field = "slug"


class DocumentViewSet(BaseViewSet):
    queryset = Document.objects.all()
    serializer_class = s.DocumentSerializer
    pagination_class = None
    filterset_fields = ["category", "year"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        is_member = (
            user.is_authenticated
            and hasattr(user, "member")
            and user.member.status == "active"
        )
        if not (is_staff(self.request) or is_member):
            qs = qs.filter(is_public=True)
        return qs


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def site_view(request):
    setting = SiteSetting.load()
    return Response(s.SiteSettingSerializer(setting, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def stats_view(request):
    from accounts.models import MemberProfile

    setting = SiteSetting.load()
    founded = setting.founded.year if setting.founded else 1975
    from datetime import date

    totals = Municipality.objects.aggregate(members=Sum("members_count"), sucos=Sum("sucos_with_structure"))
    return Response({
        "founded_year": founded,
        "years": date.today().year - founded,
        "municipalities": Municipality.objects.count(),
        "members_estimate": (totals["members"] or 0) + MemberProfile.objects.filter(status="active").count(),
        "sucos_with_structure": totals["sucos"] or 0,
        "activities": Activity.objects.filter(is_published=True).count(),
        "secretaries_general": SecretaryGeneralMandate.objects.count(),
    })


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@throttle_classes([ScopedRateThrottle])
def contact_view(request):
    serializer = s.ContactMessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"detail": "ok"}, status=201)


contact_view.cls.throttle_scope = "contact"
