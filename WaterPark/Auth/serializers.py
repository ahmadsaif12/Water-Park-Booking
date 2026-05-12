from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import User, AuthorProfile


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    role = serializers.ChoiceField(choices=["admin", "author"], default="author")

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)


class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorProfile
        fields = ["bio", "avatar", "designation", "social_links"]


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    author_profile = AuthorProfileSerializer(read_only=True)

    @extend_schema_field(serializers.CharField())
    def get_full_name(self, obj):
        return obj.full_name

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "avatar",
            "date_joined",
            "is_active",
            "author_profile",
        ]
        read_only_fields = ["id", "email", "role", "date_joined", "is_active"]
