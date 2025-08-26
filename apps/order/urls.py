
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()


urlpatterns = [
    path("orders/", views.OrderCreateListView.as_view(), name="services"),
    path("update-order-status/<int:pk>/", views.OrderStatusUpdateView.as_view(), name='update-order-status'),
    path("assign-worker-to-order/", views.WorkerAssignmentToOrderAPIView.as_view(), name='assign-worker-to-order'),
    path("pay-order/<int:pk>/", views.OrderPaymentView.as_view(), name='pay-order'),
]
