# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="auth-login"),
    path("register/", views.register, name="auth-register"),
    path("logout/", views.logout, name="auth-logout"),
    path("token/refresh/", views.token_refresh, name="auth-token-refresh"),
    path("me/", views.me, name="auth-me"),
    path("change-password/", views.change_password, name="auth-change-password"),
]
