from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Notification, UserNotification
from ..serializers import NotificationSerializer, UserNotificationSerializer


"""class MarkNotificationAsRead(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
      
        try:
            notification = Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

        user_notification, created = UserNotification.objects.get_or_create(
            notification=notification,
            user=request.user
        )

        if not created and user_notification.is_read:
            return Response({"message": "Notification already marked as read"}, status=status.HTTP_400_BAD_REQUEST)

        user_notification.is_read = True
        user_notification.save()

        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)"""

class MarkNotificationsAsRead(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            notification_ids = request.data.get('notification_ids', [])
            if not notification_ids:
                return Response({"error": "No notification IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

            UserNotification.objects.filter(
                user=request.user,
                notification_id__in=notification_ids,
                is_read=False
            ).update(is_read=True)

            return Response({"message": "Notifications marked as read"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
