from django.db import models

from apps.service.models import Service
from apps.users.models import User


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    service = models.ForeignKey(Service, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    timestamp = models.DateTimeField()
