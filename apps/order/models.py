from django.contrib.auth import get_user_model
from django.db import models

from apps.service.models import Service

User = get_user_model()


class Order(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1, "Pending"
        ACCEPTED = 2, "Accepted"
        DONE = 3, "Done"
        CANCELED = 4, "CANCELED"

    class PaymentStatus(models.IntegerChoices):
        WAITING = 1, "Waiting"
        DONE = 2, "Done"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    service = models.ForeignKey(Service, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    timestamp = models.DateTimeField()

    status = models.PositiveSmallIntegerField(choices=Status, default=Status.PENDING)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    worker = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="worker_orders", null=True, blank=True)
    payment_status = models.PositiveSmallIntegerField(choices=PaymentStatus, default=PaymentStatus.WAITING)

    long = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
