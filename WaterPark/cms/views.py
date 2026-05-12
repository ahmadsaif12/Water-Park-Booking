from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound, NotAuthenticated
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
)

from drf_spectacular.types import OpenApiTypes

from Auth.permissions import IsAdminOrAuthor

from .models import Blog, BlogCategory, BlogComment

from .serializers import (
    BlogListSerializer,
    BlogDetailSerializer,
    BlogCreateSerializer,
    BlogUpdateSerializer,
    BlogCategorySerializer,
    BlogCommentSerializer,
    BlogCommentCreateSerializer,
)


@extend_schema_view(
    get=extend_schema(
        operation_id="list_categories",
        responses=BlogCategorySerializer(many=True),
    ),
    post=extend_schema(
        operation_id="create_category",
        request=BlogCategorySerializer,
        responses=BlogCategorySerializer,
    ),
)
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def categories(request):
    if request.method == "GET":
        qs = BlogCategory.objects.filter(is_active=True)

        serializer = BlogCategorySerializer(qs, many=True)

        return Response(serializer.data)

    if not request.user.is_authenticated:
        raise NotAuthenticated()

    if not IsAdminOrAuthor().has_permission(request, None):
        raise PermissionDenied("Role not permitted.")

    serializer = BlogCategorySerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        operation_id="list_blogs",
        parameters=[
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by category slug",
                required=False,
            )
        ],
        responses=BlogListSerializer(many=True),
    ),
    post=extend_schema(
        operation_id="create_blog",
        request=BlogCreateSerializer,
        responses=BlogDetailSerializer,
    ),
)
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def blogs(request):
    if request.method == "GET":
        qs = Blog.objects.filter(is_active=True).select_related(
            "category",
            "author",
        )

        category_slug = request.query_params.get("category")

        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        serializer = BlogListSerializer(qs, many=True)

        return Response(serializer.data)

    if not request.user.is_authenticated:
        raise NotAuthenticated()

    if not IsAdminOrAuthor().has_permission(request, None):
        raise PermissionDenied("Role not permitted.")

    serializer = BlogCreateSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    blog = serializer.save(author=request.user)

    return Response(
        BlogDetailSerializer(blog).data,
        status=status.HTTP_201_CREATED,
    )


@extend_schema_view(
    get=extend_schema(
        operation_id="retrieve_blog",
        responses=BlogDetailSerializer,
    ),
    patch=extend_schema(
        operation_id="update_blog",
        request=BlogUpdateSerializer,
        responses=BlogDetailSerializer,
    ),
    delete=extend_schema(
        operation_id="delete_blog",
        responses=None,
    ),
)
@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def blog_detail(request, slug):
    try:
        blog = Blog.objects.select_related(
            "category",
            "author",
        ).get(
            slug=slug,
            is_active=True,
        )

    except Blog.DoesNotExist:
        raise NotFound("Blog not found.")

    if request.method == "GET":
        serializer = BlogDetailSerializer(blog)

        return Response(serializer.data)

    if not request.user.is_authenticated:
        raise NotAuthenticated()

    if request.user.role != "admin" and blog.author != request.user:
        raise PermissionDenied()

    if request.method == "PATCH":
        serializer = BlogUpdateSerializer(
            blog,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(BlogDetailSerializer(blog).data)

    blog.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(
        operation_id="list_comments",
        responses=BlogCommentSerializer(many=True),
    ),
    post=extend_schema(
        operation_id="create_comment",
        request=BlogCommentCreateSerializer,
        responses=BlogCommentSerializer,
    ),
)
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def comments(request, slug):
    try:
        blog = Blog.objects.get(
            slug=slug,
            is_active=True,
        )

    except Blog.DoesNotExist:
        raise NotFound("Blog not found.")

    if request.method == "GET":
        qs = blog.comments.filter(is_active=True).select_related("user")

        serializer = BlogCommentSerializer(qs, many=True)

        return Response(serializer.data)

    if not request.user.is_authenticated:
        raise NotAuthenticated()

    serializer = BlogCommentCreateSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    comment = serializer.save(
        user=request.user,
        blog=blog,
    )

    return Response(
        BlogCommentSerializer(comment).data,
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    operation_id="delete_comment",
    responses=None,
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def comment_detail(request, slug, pk):
    try:
        comment = BlogComment.objects.select_related("user").get(
            pk=pk,
            blog__slug=slug,
        )

    except BlogComment.DoesNotExist:
        raise NotFound("Comment not found.")

    if request.user.role != "admin" and comment.user != request.user:
        raise PermissionDenied()

    comment.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)
