from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from datetime import date
from misc.models import BaseModel


def get_today():
    return date.today()


def avatar_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    import uuid

    new_filename = f"{uuid.uuid4()}.{ext}"
    return f"avatars/{new_filename}"


def author_avatar_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    import uuid

    new_filename = f"{uuid.uuid4()}.{ext}"
    return f"authors/{new_filename}"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("author", "Author"),
    ]

    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="author",
        verbose_name="Role",
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_path, null=True, blank=True, verbose_name="Avatar"
    )
    date_joined = models.DateField(default=get_today, verbose_name="Date Joined")
    meta = models.JSONField(default=dict, blank=True, verbose_name="Meta")
    is_staff = models.BooleanField(default=False)  # ✅ fixed: was True
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    @property
    def username(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_or_create(cls, email, **kwargs):
        user, _ = cls.objects.get_or_create(email=email, defaults=kwargs)
        return user

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
        return self

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]


class AuthorProfile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="author_profile"
    )
    bio = models.TextField(blank=True, default="", verbose_name="Bio")
    avatar = models.ImageField(
        upload_to=author_avatar_upload_path,
        null=True,
        blank=True,
        verbose_name="Avatar",
    )
    designation = models.CharField(
        max_length=255, blank=True, verbose_name="Designation"
    )
    social_links = models.JSONField(
        default=dict, blank=True, verbose_name="Social Links"
    )

    def __str__(self):
        return f"{self.user.email} - Profile"

    class Meta:
        verbose_name = "Author Profile"
        verbose_name_plural = "Author Profiles"
