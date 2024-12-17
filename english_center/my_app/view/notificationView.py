from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from ..models import Notification, Course, Teacher
import logging
from rest_framework import status
from ..serializers import NotificationSerializer



logger = logging.getLogger(__name__)

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        notifications = Notification.objects.filter(course_id=course_id).order_by('-timestamp')
        data = [
            {
                'title': n.title,
                'message': n.message,
                'timestamp': n.timestamp,
                'teacher': n.teacher.user.username
            }
            for n in notifications
        ]
        return Response(data)