from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
import os
import uuid


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# slider image
def slider_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("slider_images/", new_filename)


# logo images
def logo_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("site_logo/", new_filename)


# user images
def user_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("testimonials_image/", new_filename)


# team images
def team_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("team_member_image/", new_filename)


class SiteInfo(models.Model):  # no timestamps needed for settings
    site_name = models.CharField(max_length=100, verbose_name="Site Name")
    site_keywords = models.CharField(max_length=225, verbose_name="Site Keywords")
    site_email = models.EmailField(verbose_name="Site Email")
    site_hr_email = models.EmailField(verbose_name="HR Email")
    site_phone = models.CharField(max_length=225, verbose_name="Site Phone")
    site_fax = models.CharField(max_length=20, verbose_name="Site FAX")
    site_address = models.CharField(max_length=255, verbose_name="Site Address")
    site_country = models.CharField(max_length=255, verbose_name="Country")
    site_city = models.CharField(max_length=255, verbose_name="City")
    site_logo = models.ImageField(
        upload_to=logo_image_upload_path, max_length=250, null=True, default=None
    )
    site_description = models.TextField(verbose_name="Site Description")

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Web Setting"
        verbose_name_plural = "Website Setting"
        ordering = ["site_name"]


class SocialMediaLinks(models.Model):
    facebook_url = models.URLField(verbose_name="Facebook URL", null=True, blank=True)
    x_url = models.URLField(verbose_name="X URL", null=True, blank=True)
    instagram_url = models.URLField(verbose_name="Instagram URL", null=True, blank=True)
    linkedIn_url = models.URLField(verbose_name="LinkedIn URL", null=True, blank=True)

    def __str__(self):
        return (
            self.facebook_url
            or self.instagram_url
            or self.x_url
            or self.linkedIn_url
            or "Social Media Links"
        )

    class Meta:
        verbose_name = "Social Media Link"
        verbose_name_plural = "Social Media Links"


class Slider(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Slider Title")
    sub_title = models.CharField(max_length=200, verbose_name="Slider Subtitle")
    description = models.TextField(verbose_name="Slider Description")
    image = models.ImageField(
        upload_to=slider_image_upload_path, max_length=250, null=True, default=None
    )
    slug = AutoSlugField(populate_from="title", unique=True, verbose_name="Slider Slug")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"
        ordering = ["title"]


class Testimonial(BaseModel):
    RATING_CHOICES = (
        (1, "★ 1 Star"),
        (2, "★★ 2 Stars"),
        (3, "★★★ 3 Stars"),
        (4, "★★★★ 4 Stars"),
        (5, "★★★★★ 5 Stars"),
    )
    name = models.CharField(max_length=100, verbose_name="Client Name")
    designation = models.CharField(max_length=100, verbose_name="Client Designation")
    feedback = models.TextField(verbose_name="Client Feedback")
    image = models.ImageField(
        upload_to=user_image_upload_path, max_length=250, null=True, default=None
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name="Client Rating", choices=RATING_CHOICES
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ["name"]


class TeamMember(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Member Name")
    designation = models.CharField(max_length=100, verbose_name="Member Designation")
    bio = models.TextField(verbose_name="Member Bio")
    image = models.ImageField(
        upload_to=team_image_upload_path, max_length=250, null=True, default=None
    )
    fb_url = models.URLField(verbose_name="Facebook URL", null=True, blank=True)
    twitter_url = models.URLField(verbose_name="Twitter URL", null=True, blank=True)
    linkedin_url = models.URLField(verbose_name="LinkedIn URL", null=True, blank=True)
    instagram_url = models.URLField(verbose_name="Instagram URL", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ["name"]


class GalleryImage(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Image Title")
    image = models.ImageField(
        upload_to="gallery_images/", max_length=250, null=True, default=None
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
        ordering = ["-created_at"]


class AboutUs(BaseModel):
    title = models.CharField(max_length=200, verbose_name="About Us Heading")
    descriptions = models.TextField(verbose_name="About Us")
    image = models.ImageField(
        upload_to="about_us/", max_length=200, null=True, default=None
    )
    years_experiences = models.CharField(
        max_length=255, verbose_name="Years of Experience"
    )
    happy_visitors = models.CharField(max_length=255, verbose_name="Happy Visitors")
    awards_winning = models.CharField(max_length=255, verbose_name="Awards Won")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"
