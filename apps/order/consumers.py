from urllib.parse import parse_qs

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class BaseJWTJsonConsumer(AsyncJsonWebsocketConsumer):
    user = None

    async def connect(self):
        from apps.order.models import User
        from rest_framework_simplejwt.tokens import AccessToken

        query_params = parse_qs(self.scope["query_string"].decode())
        token = query_params.get("token", [None])[0]

        if token:
            try:
                access_token = AccessToken(token)
                self.user = await User.objects.aget(id=access_token["user_id"])
            except Exception:
                self.user = None

        if self.user:
            await self.accept()
        else:
            await self.close(4401, "Unauthorized")


class ClientConsumer(BaseJWTJsonConsumer):
    async def connect(self):
        await super().connect()
        await self.channel_layer.group_add(f"worker_{self.user.id}", self.channel_name)


    async def disconnect(self, close_code):
        if not self.user.is_anonymous:
            await self.channel_layer.group_discard(f"worker_{self.user.id}", self.channel_name)

    async def notify_user(self, event):
        await self.send_json(event)
