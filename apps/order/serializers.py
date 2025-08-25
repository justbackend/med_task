from rest_framework import serializers

from apps.order.models import Order
from apps.service.models import Service
from apps.service.serializers import ServiceSerializer
from apps.users.models import User
from apps.users.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    service_details = ServiceSerializer(source="service", read_only=True)
    user_details = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "updated_at",
            "timestamp",
            "service",
            "user",
            "service_details",
            "user_details",
        ]
