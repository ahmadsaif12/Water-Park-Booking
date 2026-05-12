from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    SolarSchedule,
    PeriodicTask,
)
from django_celery_results.models import TaskResult, GroupResult
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from Auth.models import AuthorProfile

User = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name", "role")


@admin.register(User)
class UserAdmin(ModelAdmin, BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        "id",
        "avatar_preview",
        "first_name",
        "last_name",
        "email",
        "role",
        "is_active",
        "date_joined",
    )
    list_display_links = ("id", "avatar_preview", "first_name")
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-created_at",)
    list_per_page = 10

    fieldsets = (
        (
            "Personal Info",
            {
                "fields": ("first_name", "last_name", "role", "avatar", "date_joined"),
                "classes": ("wide",),
            },
        ),
        (
            "Login Info",
            {
                "fields": ("email", "password"),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
                "classes": ("wide",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width:50px; height:50px; object-fit:cover; border-radius:50%;" />',
                obj.avatar.url,
            )
        return "N/A"

    avatar_preview.short_description = "Photo"


@admin.register(AuthorProfile)
class AuthorProfileAdmin(ModelAdmin):
    list_display = ("user", "designation", "created_at")
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "designation",
    )


admin.site.unregister(Group)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)
