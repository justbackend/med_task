from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from apps.order.models import Order
from apps.order.serializers import OrderSerializer


class OrderCreateListView(generics.ListCreateAPIView):
    queryset = Order.objects.select_related("service", "user").all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Sizga ruhsat etilmagan.")
        serializer.save()
