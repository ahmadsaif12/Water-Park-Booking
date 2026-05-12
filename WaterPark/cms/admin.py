from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Blog, BlogCategory, BlogComment


@admin.register(BlogCategory)
class BlogCategoryAdmin(ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    actions = ["make_active", "make_inactive"]

    @admin.action(description="Activate selected")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = (
        "image_preview",
        "title",
        "category",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_display_links = ("image_preview", "title")
    search_fields = ("title", "category__name")
    list_filter = ("is_active", "category")
    actions = ["make_active", "make_inactive"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:50px; height:50px; object-fit:cover; border-radius:4px;" />',
                obj.image.url,
            )
        return "N/A"

    image_preview.short_description = "Image"

    @admin.action(description="Activate selected")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(BlogComment)
class BlogCommentAdmin(ModelAdmin):
    list_display = ("blog", "user", "is_active", "created_at")
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "blog__title",
    )
    list_filter = ("is_active",)
    actions = ["make_active", "make_inactive"]

    @admin.action(description="Activate selected")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
