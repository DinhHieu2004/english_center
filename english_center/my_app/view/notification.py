from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from ..models import Notification, Course, Teacher
import logging



logger = logging.getLogger(__name__)

class SendNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        teacher = request.user.teacher  # Xác định giáo viên
        course = Course.objects.get(id=course_id)
        
        if course.teacher != teacher:
            return Response({'error': 'Bạn không có quyền gửi thông báo cho lớp này'}, status=403)
        
        message = request.data.get('message')
        if not message:
            return Response({'error': 'Thông báo không được để trống'}, status=400)

        # Lưu thông báo vào DB
        Notification.objects.create(
            title="Thông báo từ giáo viên",
            course=course,
            teacher=teacher,
            message=message,
        )

        # Gửi thông báo qua WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"course_{course_id}",
            {
                'type': 'send_notification',
                'message': message,
            }
        )
        return Response({'success': 'Thông báo đã được gửi'}, status=200)
