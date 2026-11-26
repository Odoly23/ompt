"""Member-facing endpoints: card verification, dues, registrations, announcements."""
from datetime import date

from django.conf import settings
from django.db.models import Q
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from comms.models import Announcement
from dues.models import DuesRate, member_balance
from events.api import MyRegistrationSerializer

from .models import MemberProfile


def card_url(member):
    return f"{settings.SITE_URL.rstrip('/')}/verifika/{member.card_token}"


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
@throttle_classes([ScopedRateThrottle])
def verify_card(request, token):
    """Public check of a member card (QR). Shows only what a door-keeper needs."""
    member = MemberProfile.objects.select_related("municipality").filter(card_token=token).first()
    if not member:
        return Response({"valid": False, "reason": "unknown"}, status=404)
    due, paid, outstanding = member_balance(member, date.today().year)
    return Response({
        "valid": member.status == "active",
        "status": member.status,
        "full_name": member.full_name,
        "member_number": member.member_number,
        "municipality": member.municipality.name,
        "photo": request.build_absolute_uri(member.photo.url) if member.photo else None,
        "dues_up_to_date": outstanding == 0,
    })


verify_card.cls.throttle_scope = "verify"


def _member(request):
    return getattr(request.user, "member", None)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_overview(request):
    """Everything the member dashboard needs in one call."""
    member = _member(request)
    if not member:
        return Response({"detail": "Konta ne'e la iha perfil membru."}, status=400)

    year = date.today().year
    years = sorted({year, *member.payments.values_list("year", flat=True), member.created_at.year})
    dues = []
    for y in years:
        due, paid, outstanding = member_balance(member, y)
        dues.append({"year": y, "due": str(due), "paid": str(paid), "outstanding": str(outstanding)})
    payments = [
        {"year": p.year, "amount": str(p.amount), "paid_on": p.paid_on, "method": p.get_method_display(), "receipt_number": p.receipt_number}
        for p in member.payments.all()
    ]

    regs = member.registrations.select_related("event").exclude(status="cancelled").order_by("event__starts_at")
    ann_filter = Q(status="sent") & (Q(municipality__isnull=True) | Q(municipality=member.municipality))
    if member.status != "active":
        ann_filter &= Q(audience="all")
    announcements = Announcement.objects.filter(ann_filter)[:20]

    rate = DuesRate.for_year(year)
    return Response({
        "card": {
            "token": str(member.card_token),
            "verify_url": card_url(member),
        } if member.status == "active" else None,
        "dues": {"current_rate": str(rate.annual_amount) if rate else None, "years": dues, "payments": payments},
        "registrations": MyRegistrationSerializer(regs, many=True, context={"request": request}).data,
        "announcements": [
            {"id": a.id, "title": a.title, "body": a.body, "sent_at": a.sent_at,
             "scope": a.municipality.name if a.municipality else None}
            for a in announcements
        ],
    })
