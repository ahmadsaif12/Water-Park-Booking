from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Blog, BlogCategory, BlogComment
from Auth.serializers import UserSerializer


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ["id", "name", "slug", "is_active"]


class BlogListSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "author",
            "image",
            "is_active",
            "created_at",
        ]


class BlogDetailSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    author = UserSerializer(read_only=True)
    total_comments = serializers.SerializerMethodField()

    @extend_schema_field(serializers.IntegerField())
    def get_total_comments(self, obj):
        return obj.comments.filter(is_active=True).count()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "author",
            "content",
            "image",
            "is_active",
            "total_comments",
            "created_at",
            "updated_at",
        ]


class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["title", "category", "content", "image"]


class BlogUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["title", "category", "content", "image", "is_active"]


class BlogCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BlogComment
        fields = ["id", "blog", "user", "message", "is_active", "created_at"]
        read_only_fields = ["id", "user", "is_active", "created_at"]


class BlogCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = ["message"]
