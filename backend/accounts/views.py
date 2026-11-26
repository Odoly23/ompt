from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import MemberProfile
from .serializers import (
    ChangePasswordSerializer, EmailTokenSerializer, MemberProfileSerializer, RegisterSerializer,
    UserSerializer,
)


class LoginView(TokenObtainPairView):
    serializer_class = EmailTokenSerializer
    throttle_scope = "auth"


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = "register"

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        refresh = RefreshToken.for_user(member.user)
        return Response(
            {
                "user": UserSerializer(member.user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        member = getattr(request.user, "member", None)
        if member is None:
            return Response({"detail": "Konta ne'e la iha perfil membru."}, status=400)
        serializer = MemberProfileSerializer(member, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": ["Password tuan la loos."]}, status=400)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Password troka ona."})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            RefreshToken(request.data.get("refresh")).blacklist()
        except (TokenError, TypeError):
            return Response({"detail": "Refresh token la válidu."}, status=400)
        return Response(status=204)


class MemberCardView(APIView):
    """Data for the digital membership card (active members only)."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        member = getattr(request.user, "member", None)
        if not member or member.status != "active":
            return Response({"detail": "Kartaun disponível deit ba membru ativu."}, status=403)
        return Response(MemberProfileSerializer(member).data)
