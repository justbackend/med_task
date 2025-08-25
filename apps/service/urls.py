from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()


urlpatterns = [
    path("services/", views.ServiceView.as_view(), name="services"),
]
