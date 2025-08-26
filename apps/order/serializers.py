from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.order.models import Order
from apps.service.models import Service
from apps.service.serializers import ServiceSerializer
from apps.users.serializers import UserSerializer
from apps.utils.notifier import notify

User = get_user_model()



class OrderSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    worker = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    service_details = ServiceSerializer(source="service", read_only=True)
    user_details = UserSerializer(source="user", read_only=True)
    worker_datils = UserSerializer(source="worker", read_only=True)


    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "updated_at",
            "timestamp",
            "service",
            "user",
            "status",
            "price",
            "worker",
            "payment_status",
            "long",
            "lat",
            "service_details",
            "user_details",
            "worker_datils",
        ]

        extra_kwargs = {
            "status": {"read_only": True},
            "payment_status": {"read_only": True}
        }

    def create(self, validated_data):
        order = super().create(validated_data)
        worker = order.worker

        data = {
            "order_id": order.id,
            "price": str(order.price),
            "service": order.service.name,
        }


        notify(worker.id, data)
        return order


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def update(self, instance, validated_data):
        if validated_data['status'] == Order.Status.DONE:
            instance.payment_status = Order.PaymentStatus.DONE

        if validated_data['status'] != instance.status:
            data = {
                "order_id": instance.id,
                "old_status": instance.status,
                "new_status": validated_data['status'],
            }

            notify(instance.user.id, data)


        return super().update(instance, validated_data)


class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id']

    def update(self, instance, validated_data):
        instance.payment_status = Order.PaymentStatus.DONE
        instance.save()
        return instance



class WorkerAssignmentToOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    worker_id = serializers.IntegerField()
