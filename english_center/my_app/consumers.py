import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Notification, Teacher, Course
from django.utils.timezone import now
import traceback
from channels.db import database_sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.course_id = self.scope['url_route']['kwargs']['course_id']
            self.room_group_name = f'course_{self.course_id}'
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            print(f"WebSocket connected for course {self.course_id}")
        except Exception as e:
            print(f"Connection error: {str(e)}")
            print(traceback.format_exc())

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            print(f"WebSocket disconnected with code: {close_code}")
        except Exception as e:
            print(f"Disconnection error: {str(e)}")

    @database_sync_to_async 
    def create_notification(self, title, message, sender_id, course_id):
        try:
            # Giữ thao tác đồng bộ ở đây
            teacher = Teacher.objects.get(id=sender_id)
            course = Course.objects.get(id=course_id)
            
            notification = Notification.objects.create(
                title=title,
                message=message,
                teacher=teacher,
                course=course,
                timestamp=now()
            )
            print(f"Notification created: {notification}")
            return True
        except Exception as e:
            print(f"Database error: {str(e)}")
            print(traceback.format_exc())
            return False
  
    async def receive(self, text_data):
        try:
            print(f"Received data: {text_data}")
            text_data_json = json.loads(text_data)
            title = text_data_json['title']
            message = text_data_json['content']
            sender = text_data_json['sender']
            time = text_data_json['time']

            # save
            success = await self.create_notification(
                title=title, 
                message=message, 
                sender_id=sender, 
                course_id=self.course_id
            )

            if success:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'send_notification',
                        'title': title,
                        'content': message,
                        'sender': sender,
                        'time': time,
                    }
                )
                print("Notification sent to group successfully")
            else:
                print("Failed to save notification")

        except Exception as e:
            print(f"Receive error: {str(e)}")
            print(traceback.format_exc())

    async def send_notification(self, event):
        try:
            await self.send(text_data=json.dumps({
                'title': event['title'],
                'content': event['content'],
                'sender': event['sender'],
                'time': event['time'],
            }))
            print("Notification sent to WebSocket successfully")
        except Exception as e:
            print(f"Send error: {str(e)}")
            print(traceback.format_exc())

      # daphne -b 0.0.0.0 -p 8000 english_center.asgi:application  