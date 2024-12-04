from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import TeacherSerializer, CourseSerialozer, StudentSerializer, AttendanceSerializer
from ..models import Course, Teacher, Student, Attendance, CourseSchedule
from rest_framework.exceptions import NotFound
from datetime import datetime


class AttendanceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, course_id):
        attendance_list = Attendance.objects.filter(course_id=course_id)
        
        if not attendance_list:
            raise NotFound(detail="No attendance found for this course")
        
        serializer = AttendanceSerializer(attendance_list, many=True)
        return Response(serializer.data)
    
class CourseScheduleListView(APIView):
    def get(self, request, course_id):
        try:
            # Lấy khóa học
            course = Course.objects.get(id=course_id)
            start_date = course.start_date  # Ngày bắt đầu khóa học
            total_sessions = course.total_session  # Tổng số buổi học
            
            schedules = CourseSchedule.objects.filter(course=course)  # Các lịch học của khóa học

            all_class_dates = []

            for schedule in schedules:
                # Tính toán ngày học cho từng lịch học trong tuần
                class_dates = schedule.get_next_class_dates(start_date, total_sessions)
                all_class_dates.extend(class_dates)
            
            # Trả về dữ liệu ngày học đã tính
            return Response({
                "class_dates": [date.strftime('%d-%m') for date in all_class_dates]
            })
        
        except Course.DoesNotExist:
            return Response({"detail": "Khóa học không tồn tại."})