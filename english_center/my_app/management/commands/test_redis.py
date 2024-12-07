from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Command(BaseCommand):
    help = "Test Redis connection"

    def handle(self, *args, **kwargs):
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_add)(
                "test_group", "test_channel"
            )
            async_to_sync(channel_layer.group_send)(
                "test_group", {"type": "test.message", "message": "Hello, Redis!"}
            )
            self.stdout.write(self.style.SUCCESS("Redis connection is working correctly!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
