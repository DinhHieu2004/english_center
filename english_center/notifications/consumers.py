import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Tạo nhóm người dùng cho WebSocket
        self.group_name = "notifications_group"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Xóa nhóm khi ngắt kết nối
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Nhận dữ liệu từ WebSocket
        data = json.loads(text_data)
        message = data['message']

        # Gửi tin nhắn đến nhóm
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_notification',
                'message': message
            }
        )

    async def send_notification(self, event):
        # Gửi dữ liệu trở lại WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
