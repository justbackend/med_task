from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from apps.service.models import Service
from apps.service.serializers import ServiceSerializer


class ServiceView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Sizga ruhsat etilmagan.")
        serializer.save()
