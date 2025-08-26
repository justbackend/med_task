from django.urls import path

from apps.order.consumers import ClientConsumer

websocket_urlpatterns = [
    path("ws/client/", ClientConsumer.as_asgi()),
]
