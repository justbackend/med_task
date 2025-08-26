from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Service(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100)
