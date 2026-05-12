from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
import os
import uuid

from misc.models import BaseModel
from Auth.models import User


def blog_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("blog_images/", new_filename)


class BlogCategory(BaseModel):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from="name", unique=True, always_update=False, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["-created_at"]


class Blog(BaseModel):
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blogs",
    )
    title = models.CharField(max_length=200)
    slug = AutoSlugField(
        populate_from="title", unique=True, always_update=False, null=True, blank=True
    )
    content = HTMLField(verbose_name="Blog Content")
    image = models.ImageField(
        upload_to=blog_image_upload_path, max_length=250, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"{self.title} ({self.category.name if self.category else 'No Category'})"
        )

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ["-created_at"]


class BlogComment(BaseModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="comments"
    )
    message = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.user.full_name if self.user else 'Anonymous'} on {self.blog.title}"

    class Meta:
        verbose_name = "Blog Comment"
        verbose_name_plural = "Blog Comments"
        ordering = ["-created_at"]
