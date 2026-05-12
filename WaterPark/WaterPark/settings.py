"""
Django settings for WaterPark project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
from django.templatetags.static import static
from django.urls import reverse_lazy

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# core config
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-default-key-change-me")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ROOT_URLCONF = "WaterPark.urls"
WSGI_APPLICATION = "WaterPark.wsgi.application"
AUTH_USER_MODEL = "Auth.User"


INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "tinymce",
    "autoslug",
    "widget_tweaks",
    "django_celery_beat",
    "django_celery_results",
    "drf_spectacular",
    # Local
    "misc",
    "Auth",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# database config
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "waterpark_db"),
        "USER": os.getenv("DB_USER", "waterpark_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "waterpark_pass"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# jwt config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}


# DRF
SPECTACULAR_SETTINGS = {
    "TITLE": "WaterPark API",
    "DESCRIPTION": "API documentation for the WaterPark booking system",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SECURITY": [{"bearerAuth": []}],
    "COMPONENTS": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
}

# unfold admin
UNFOLD = {
    "SITE_TITLE": "WaterPark",
    "SITE_HEADER": "WaterPark Admin",
    "SITE_SUBHEADER": "Management Panel",
    "SITE_URL": "/",
    "SITE_SYMBOL": "water",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "THEME": "dark",
    "COLORS": {
        "primary": {
            "50": "254 242 242",  # Red shades - Primary color
            "100": "254 226 226",
            "200": "254 202 202",
            "300": "252 165 165",
            "400": "248 113 113",
            "500": "239 68 68",  # Main Red
            "600": "220 38 38",  # Dark Red
            "700": "185 28 28",
            "800": "153 27 27",
            "900": "127 29 29",
            "950": "69 10 10",
        },
        "danger": {
            "50": "23 37 84",  # Dark Blue shades - Background color
            "100": "30 58 138",
            "200": "30 64 175",
            "300": "29 78 216",
            "400": "37 99 235",
            "500": "30 64 175",  # Main Dark Blue
            "600": "23 37 84",  # Darker Blue
            "700": "15 23 42",  # Very Dark Blue
            "800": "15 23 42",
            "900": "15 23 42",
            "950": "15 23 42",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Dashboard",
                "items": [
                    {
                        "title": "Home",
                        "icon": "home",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "Users",
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "people",
                        "link": reverse_lazy("admin:Auth_user_changelist"),
                    },
                    {
                        "title": "Author Profiles",
                        "icon": "person_edit",
                        "link": reverse_lazy("admin:Auth_authorprofile_changelist"),
                    },
                ],
            },
            {
                "title": "Website Content",
                "separator": True,
                "items": [
                    {
                        "title": "Site Info",
                        "icon": "info",
                        "link": reverse_lazy("admin:misc_siteinfo_changelist"),
                    },
                    {
                        "title": "About Us",
                        "icon": "description",
                        "link": reverse_lazy("admin:misc_aboutus_changelist"),
                    },
                    {
                        "title": "Sliders",
                        "icon": "slideshow",
                        "link": reverse_lazy("admin:misc_slider_changelist"),
                    },
                    {
                        "title": "Gallery",
                        "icon": "photo_library",
                        "link": reverse_lazy("admin:misc_galleryimage_changelist"),
                    },
                    {
                        "title": "Testimonials",
                        "icon": "rate_review",
                        "link": reverse_lazy("admin:misc_testimonial_changelist"),
                    },
                    {
                        "title": "Team Members",
                        "icon": "groups",
                        "link": reverse_lazy("admin:misc_teammember_changelist"),
                    },
                    {
                        "title": "Social Media",
                        "icon": "share",
                        "link": reverse_lazy("admin:misc_socialmedialinks_changelist"),
                    },
                ],
            },
        ],
    },
}

# lang
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# static
STATIC_URL = "static/"
STATIC_ROOT = "/vol/static"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = "media/"
MEDIA_ROOT = "/vol/media"


# celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE


# cors config
_origins = os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:8000").split(",")
CORS_ALLOWED_ORIGINS = _origins
CSRF_TRUSTED_ORIGINS = _origins

# payment config
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
