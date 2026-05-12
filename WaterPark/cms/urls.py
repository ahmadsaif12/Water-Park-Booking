from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.categories, name="blog-categories"),
    path("blogs/", views.blogs, name="blogs"),
    path("blogs/<slug:slug>/", views.blog_detail, name="blog-detail"),
    path("blogs/<slug:slug>/comments/", views.comments, name="blog-comments"),
    path(
        "blogs/<slug:slug>/comments/<int:pk>/",
        views.comment_detail,
        name="blog-comment-detail",
    ),
]
