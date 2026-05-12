from django.contrib import admin
from django.utils.html import format_html

from misc.models import (
    TeamMember,
    Testimonial,
    Slider,
    SiteInfo,
    GalleryImage,
    AboutUs,
    SocialMediaLinks,
)


def display_field(field_name, title):
    def func(self, obj):
        return getattr(obj, field_name)

    func.short_description = title
    return func


class SiteInfoAdmin(admin.ModelAdmin):
    list_display = (
        "site_name_display",
        "site_email_display",
        "site_hr_email_display",
        "site_fax_display",
        "site_address_display",
        "site_contry",
        "site_city",
        "image_tag",
    )
    site_name_display = display_field("site_name", "Company Name")
    site_email_display = display_field("site_email", "Email")
    site_hr_email_display = display_field("site_hr_email", "HR Email")
    site_phone_display = display_field("site_phone", "Phone")
    site_fax_display = display_field("site_fax", "Fax No")
    site_address_display = display_field("site_address", "Company Address")
    site_contry_display = display_field("site_contry", "Country")
    site_city_display = display_field("site_city", "City")

    def image_tag(self, obj):
        if obj.site_logo:
            return format_html(
                '<img src="{}" width="50" height="50" />', obj.site_logo.url
            )
        return "-"

    image_tag.short_description = "Logo"

    def has_add_permission(self, request):
        if SiteInfo.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(SiteInfo, SiteInfoAdmin)


class SocialMediaLinksAdmin(admin.ModelAdmin):
    list_display = (
        "facebook_url_display",
        "x_url_display",
        "instagram_url_display",
        "linkedIn_url_display",
    )

    def facebook_url_display(self, obj):
        return obj.facebook_url if obj.facebook_url else "N/A"

    facebook_url_display.short_description = "Facebook URL"

    def x_url_display(self, obj):
        return obj.x_url if obj.x_url else "N/A"

    x_url_display.short_description = "X URL"

    def instagram_url_display(self, obj):
        return obj.instagram_url if obj.instagram_url else "N/A"

    instagram_url_display.short_description = "Instagram URL"

    def linkedIn_url_display(self, obj):
        return obj.linkedIn_url if obj.linkedIn_url else "N/A"

    linkedIn_url_display.short_description = "LinkedIn URL"

    def has_add_permission(self, request):
        if SocialMediaLinks.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(SocialMediaLinks, SocialMediaLinksAdmin)


class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "sub_title", "image_tag")

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="50" />', obj.image.url
            )
        return "-"

    image_tag.short_description = "Slider Image"


admin.site.register(Slider, SliderAdmin)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "rating_stars", "image_tag", "is_active")
    actions = ["make_active", "make_inactive"]

    @admin.action(description="Activate selected")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    def rating_stars(self, obj):
        filled = "★" * obj.rating
        empty = "☆" * (5 - obj.rating)
        return format_html(
            '<span style="color: gold; font-size:16px;">{}</span>'
            '<span style="color: #ccc; font-size:16px;">{}</span>',
            filled,
            empty,
        )

    rating_stars.short_description = "Rating"

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "-"

    image_tag.short_description = "Client Image"


admin.site.register(Testimonial, TestimonialAdmin)


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "image_tag", "is_active")
    actions = ["make_active", "make_inactive"]

    @admin.action(description="Activate selected")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "-"

    image_tag.short_description = "Member Image"


admin.site.register(TeamMember, TeamMemberAdmin)


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "image_tag")

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="50" />', obj.image.url
            )
        return "-"

    image_tag.short_description = "Gallery Image"


admin.site.register(GalleryImage, GalleryImageAdmin)


class AboutUsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "image_tag",
        "years_experiences",
        "happy_visitors",
        "awards_winning",
        "updated_at",
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="50" />', obj.image.url
            )
        return "-"

    image_tag.short_description = "Banner Image"

    def has_add_permission(self, request):
        if AboutUs.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(AboutUs, AboutUsAdmin)
