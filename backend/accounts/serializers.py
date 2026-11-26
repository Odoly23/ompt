from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import MemberProfile

User = get_user_model()


class MemberProfileSerializer(serializers.ModelSerializer):
    municipality_name = serializers.CharField(source="municipality.name", read_only=True)
    administrative_post_name = serializers.CharField(source="administrative_post.name", read_only=True, default=None)
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = MemberProfile
        exclude = ("user",)
        read_only_fields = ("member_number", "status", "status_note", "approved_at", "created_at", "accepts_statutes")


class UserSerializer(serializers.ModelSerializer):
    member = MemberProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "is_staff", "member")


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=60)
    password = serializers.CharField(write_only=True, min_length=8)
    birth_date = serializers.DateField()
    municipality = serializers.IntegerField()
    administrative_post = serializers.IntegerField(required=False, allow_null=True)
    suco = serializers.CharField(max_length=80, required=False, allow_blank=True)
    aldeia = serializers.CharField(max_length=80, required=False, allow_blank=True)
    occupation = serializers.CharField(max_length=120, required=False, allow_blank=True)
    preferred_language = serializers.ChoiceField(choices=["tet", "pt", "id", "en"], default="tet")
    accepts_statutes = serializers.BooleanField()

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Email ne'e rejista tiha ona. Halo login ka uza email seluk.")
        return value

    def validate_birth_date(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 16:
            raise serializers.ValidationError("Tuir Estatutu Art. 6, membru OPMT tenke iha tinan 16 ka liu.")
        return value

    def validate_accepts_statutes(self, value):
        if not value:
            raise serializers.ValidationError("Tenke simu prinsípiu no estatutu OPMT nian atu sai membru.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        from content.models import AdministrativePost, Municipality

        try:
            attrs["municipality"] = Municipality.objects.get(pk=attrs["municipality"])
        except Municipality.DoesNotExist:
            raise serializers.ValidationError({"municipality": "Munisípiu la iha."})
        post_id = attrs.get("administrative_post")
        if post_id:
            try:
                attrs["administrative_post"] = AdministrativePost.objects.get(
                    pk=post_id, municipality=attrs["municipality"]
                )
            except AdministrativePost.DoesNotExist:
                raise serializers.ValidationError({"administrative_post": "Postu la pertense ba munisípiu ne'e."})
        else:
            attrs["administrative_post"] = None
        return attrs

    @transaction.atomic
    def create(self, data):
        password = data.pop("password")
        email = data.pop("email")
        names = data["full_name"].split(" ", 1)
        user = User.objects.create_user(
            username=email, email=email, password=password,
            first_name=names[0], last_name=names[1] if len(names) > 1 else "",
        )
        return MemberProfile.objects.create(user=user, **data)


class EmailTokenSerializer(TokenObtainPairSerializer):
    """Login with email + password. Adds basic claims to the token."""

    def validate(self, attrs):
        attrs[self.username_field] = attrs.get(self.username_field, "").lower()
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["name"] = user.get_full_name()
        token["is_staff"] = user.is_staff
        return token


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate_new_password(self, value):
        validate_password(value, self.context["request"].user)
        return value
