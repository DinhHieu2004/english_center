
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from ..models import Notification, Course, Teacher, Attendance, UserNotification, CourseEnrollment
import logging
from rest_framework import status
from ..serializers import NotificationSerializer, UserNotificationSerializer


import logging

logger = logging.getLogger(__name__)

class NotificationListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        
        try:
            course = Course.objects.get(id=course_id)
            notifications = course.notifications.all()
            
            notifications_data = []
            for notification in notifications:
                user_notification = UserNotification.objects.filter(notification=notification, user=request.user).first()
                is_read = user_notification.is_read if user_notification else False
                notifications_data.append({
                    'id': notification.id,
                    'title': notification.title,
                    'content': notification.content,
                    'created_by': notification.created_by.username, 
                    'created_at': notification.created_at,
                    'is_read': is_read
                })

            return Response(notifications_data, status=status.HTTP_200_OK)

        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        is_student = CourseEnrollment.objects.filter(course=course, student__user=request.user).exists()
        is_teacher = course.teacher and course.teacher.user == request.user

        if not (is_student or is_teacher):
            return Response({"error": "Bạn không phải là thành viên của lớp học này."}, status=status.HTTP_403_FORBIDDEN)

        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save(created_by=request.user, course=course)

            students = CourseEnrollment.objects.filter(course=course)
            for enrollment in students:
                UserNotification.objects.get_or_create(
                    user=enrollment.student.user, 
                    notification=notification, 
                    is_read=False
                )

            if course.teacher and course.teacher.user:
                UserNotification.objects.get_or_create(
                    user=course.teacher.user, 
                    notification=notification,
                    defaults={'is_read': False}
                )

            user_notification, created = UserNotification.objects.get_or_create(
                user=request.user,
                notification=notification
            )
            if not created:
                user_notification.is_read = True
                user_notification.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteUserNotification(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, notification_id):
        
        try:
            user_notification = UserNotification.objects.get(notification_id=notification_id, user=request.user)
        except UserNotification.DoesNotExist:
            return Response({"error": "User notification not found"}, status=status.HTTP_404_NOT_FOUND)

        user_notification.delete()
        return Response({"message": "Notification deleted"}, status=status.HTTP_200_OK)    
    

class UnreadNotifications(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        unread_notifications = UserNotification.objects.filter(user=request.user, is_read=False)
        serializer = UserNotificationSerializer(unread_notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
class UserNotificationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        user_notifications = UserNotification.objects.filter(user=request.user)
        serializer = UserNotificationSerializer(user_notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
class CheckNewNotifications(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        students = CourseEnrollment.objects.filter(course=course)

        unread_notifications = UserNotification.objects.filter(
            notification__course=course,
            is_read=False,
            user=request.user
        )

        if unread_notifications.exists():
            return Response({"has_new_notification": True}, status=status.HTTP_200_OK)
        else:
            return Response({"has_new_notification": False}, status=status.HTTP_200_OK)