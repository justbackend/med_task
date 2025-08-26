# ruff: noqa: ERA001, E501
"""Base settings to build other settings files upon."""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "apps"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    env.read_env(str(BASE_DIR / ".env"))


DEBUG = env.bool("DJANGO_DEBUG", False)
TIME_ZONE = "Asia/Tashkent"
LANGUAGE_CODE = "uz"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": env.str("POSTGRES_DB"),
#         "USER": env.str("POSTGRES_USER"),
#         "PASSWORD": env.str("POSTGRES_PASSWORD"),
#         "HOST": env.str("POSTGRES_HOST"),
#         "PORT": env.str("POSTGRES_PORT"),
#     },
# }

# DATABASES["default"]["ATOMIC_REQUESTS"] = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [str(BASE_DIR / "locale")]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    # "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "rest_framework_simplejwt",
    "django_cleanup.apps.CleanupConfig",
    "django_filters",
]

LOCAL_APPS = [
    "apps.users",
    "apps.service",
    "apps.order",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIGRATION_MODULES = {"sites": "apps.contrib.sites.migrations"}

AUTH_USER_MODEL = "users.User"


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
#     },
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "apps.utils.middlewares.DisableSessionForAPIMiddleware",
]

STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATIC_URL = "/static/"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


MEDIA_ROOT = str(APPS_DIR / "media")
MEDIA_URL = "/media/"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)


ADMIN_URL = "admin/"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/3")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PERMISSION_CLASSES": ("apps.utils.permissions.RolePermission",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Your Project Name API",
    "DESCRIPTION": "Documentation of API endpoints of Your Project",
    "VERSION": "1.0.0",
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_SPLIT_RESPONSE": True,
    "COMPONENT_SPLIT_PATH": True,
    # "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    "DISABLE_ERRORS_AND_WARNINGS": True,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]/",
    # "SCHEMA_PATH_PREFIX": r"/api/v[0-9]/[a-zA-Z0-9_]+/",
}

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True
ANONYMOUS_USER_ID = -1
SECURE_SSL_REDIRECT = False

APPEND_SLASH = True
