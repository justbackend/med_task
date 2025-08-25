from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import UserRegistrationView

router = DefaultRouter()

router.register(r"", views.UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationView.as_view(), name="register"),
]
