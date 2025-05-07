from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    # path("users/", include("apps.users.urls", namespace="users")),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    path("api/v1/user/", include("apps.users.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api-schema")),
    path("api/v1/token/", TokenObtainPairView.as_view()),
    path("api/v1/refresh_token/", TokenRefreshView.as_view()),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [*urlpatterns, path("__debug__/", include(debug_toolbar.urls))]

    if "silk" in settings.INSTALLED_APPS:
        urlpatterns = [
            *urlpatterns,
            path("silk/", include("silk.urls", namespace="silk")),
        ]
