from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    class Role(models.IntegerChoices):
        ADMIN = 1, 'Admin'
        WORKER = 2, "Worker"
        CLIENT = 3, 'Client'

    role = models.PositiveSmallIntegerField(choices=Role)


