from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from drf_spectacular.openapi import AutoSchema
import rest_framework.fields as fields
from django.contrib.auth import authenticate

from .models import User, AuthorProfile
from .serializers import (
    UserSerializer,
    AuthorProfileSerializer,
    LoginSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@extend_schema(
    summary="Login",
    description="Authenticate with email and password. Returns JWT access and refresh tokens.",
    request=LoginSerializer,
    responses={
        200: inline_serializer(
            name="LoginResponse",
            fields={
                "tokens": inline_serializer(
                    name="TokenPair",
                    fields={
                        "access": fields.CharField(),
                        "refresh": fields.CharField(),
                    },
                ),
                "user": UserSerializer(),
            },
        ),
        401: OpenApiResponse(description="Invalid credentials"),
        403: OpenApiResponse(description="Account disabled"),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(
        request,
        username=serializer.validated_data["email"],
        password=serializer.validated_data["password"],
    )
    if not user:
        return Response(
            {"detail": "Invalid email or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if not user.is_active:
        return Response(
            {"detail": "Account is disabled."}, status=status.HTTP_403_FORBIDDEN
        )

    return Response(
        {"tokens": get_tokens_for_user(user), "user": UserSerializer(user).data}
    )


@extend_schema(
    summary="Register",
    description="Register a new user. Role defaults to 'author'. Creates AuthorProfile automatically.",
    request=RegisterSerializer,
    responses={
        201: inline_serializer(
            name="RegisterResponse",
            fields={
                "tokens": inline_serializer(
                    name="RegisterTokenPair",
                    fields={
                        "access": fields.CharField(),
                        "refresh": fields.CharField(),
                    },
                ),
                "user": UserSerializer(),
            },
        ),
        400: OpenApiResponse(description="Validation error"),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    user = User.objects.create_user(
        email=data["email"],
        password=data["password"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        role=data.get("role", "author"),
    )
    if user.role == "author":
        AuthorProfile.objects.create(user=user)

    return Response(
        {"tokens": get_tokens_for_user(user), "user": UserSerializer(user).data},
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    summary="Logout",
    description="Blacklist the refresh token to log out.",
    request=inline_serializer(
        name="LogoutRequest",
        fields={"refresh": fields.CharField()},
    ),
    responses={
        205: OpenApiResponse(description="Logged out successfully"),
        400: OpenApiResponse(description="Invalid or expired token"),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response(
            {"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        RefreshToken(refresh_token).blacklist()
    except TokenError:
        return Response(
            {"detail": "Token is invalid or already blacklisted."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        {"detail": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT
    )


@extend_schema(
    summary="Refresh Access Token",
    description="Provide a valid refresh token to get a new access token.",
    request=inline_serializer(
        name="TokenRefreshRequest",
        fields={"refresh": fields.CharField()},
    ),
    responses={
        200: inline_serializer(
            name="TokenRefreshResponse",
            fields={"access": fields.CharField()},
        ),
        400: OpenApiResponse(description="Invalid or expired refresh token"),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def token_refresh(request):
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response(
            {"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        token = RefreshToken(refresh_token)
        return Response({"access": str(token.access_token)})
    except TokenError:
        return Response(
            {"detail": "Token is invalid or expired."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(
    summary="Get / Update Current User",
    description="GET returns the logged-in user's profile. PATCH updates first_name, last_name, or avatar.",
    request=UserSerializer,
    responses={
        200: UserSerializer,
        400: OpenApiResponse(description="Validation error"),
        401: OpenApiResponse(description="Not authenticated"),
    },
)
@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me(request):
    if request.method == "GET":
        return Response(UserSerializer(request.user).data)

    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data)


@extend_schema(
    summary="Change Password",
    description="Change the current user's password. Requires old password for verification.",
    request=ChangePasswordSerializer,
    responses={
        200: OpenApiResponse(description="Password changed successfully"),
        400: OpenApiResponse(description="Validation error or wrong old password"),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if not request.user.check_password(serializer.validated_data["old_password"]):
        return Response(
            {"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST
        )

    request.user.set_password(serializer.validated_data["new_password"])
    request.user.save()
    return Response({"detail": "Password changed successfully."})
