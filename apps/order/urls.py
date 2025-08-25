from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()


urlpatterns = [
    path("orders/", views.OrderCreateListView.as_view(), name="services"),
]
