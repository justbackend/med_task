# ruff: noqa: E501
from datetime import timedelta

from .base import *  # noqa: F403
from .base import INSTALLED_APPS
from .base import MIDDLEWARE
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="zjW3iURogJGK5jDVLc7EQJxtvwDKulFpvqezW2YPiSGotKosJmqyjwwowJv3hYMi",
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     "default": env.db(
#         "DATABASE_URL",
#         default="postgres:///app",
#     ),
# }


# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]  # noqa: S104

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "",
#     },
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
            "IGNORE_EXCEPTIONS": True,
        },
        "TIMEOUT": None,
    },
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = env(
#     "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend",
# )

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic", *INSTALLED_APPS]


# django-toolbar
# -------------------------------------------------------------------------------
# INSTALLED_APPS += ["debug_toolbar"]
#
# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
#
# DEBUG_TOOLBAR_CONFIG = {
#     "DISABLE_PANELS": [
#         "debug_toolbar.panels.redirects.RedirectsPanel",
#         # Disable profiling panel due to an issue with Python 3.12:
#         # https://github.com/jazzband/django-debug-toolbar/issues/1875
#          "debug_toolbar.panels.profiling.ProfilingPanel",
#     ],
#     "SHOW_TEMPLATE_CONTEXT": True,
# }
# INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]


# django-silk
# ---------------------------------------------------------------------------------

INSTALLED_APPS += ['silk']

MIDDLEWARE +=['silk.middleware.SilkyMiddleware']


# ----------------------------------------------------------------------------------


# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]

# Your stuff...
# ------------------------------------------------------------------------------

# REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ('rest_framework.permissions.AllowAny',)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=10),
}
