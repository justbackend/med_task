from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def notify(user_id: int, data: dict):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"worker_{user_id}",
        {
            "type": "notify_user",
            "data": data,
        },
    )
