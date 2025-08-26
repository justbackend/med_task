from rest_framework import generics

from apps.order.models import User
from apps.service.models import Service
from apps.service.serializers import ServiceSerializer


class ServiceView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    allowed_roles = [User.Role.ADMIN]
