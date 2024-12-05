from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import TeacherSerializer, CourseSerialozer, StudentSerializer, AttendanceSerializer
from ..models import Course, Teacher, Student, Attendance, CourseSchedule
from rest_framework.exceptions import NotFound
from datetime import datetime



class AttendanceList(APIView):
    def get(self, request, course_id):
        student = request.GET.get('student')
        date = request.GET.get('date')

        # Validate required parameters
        if not student or not date:
            return Response(
                {"error": "Both 'student' and 'date' parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
        # Try to fetch the attendance record
            attendance = Attendance.objects.get(course_id=course_id, student_id=student, date=date)
            return Response({
                "status": attendance.status,
                "student": attendance.student.id,
                "date": attendance.date
            })
        except Attendance.DoesNotExist:
             return Response({
                "message": "Attendance record not found for the given student and date.",
                "status": "",
                "student": student,
                "date": date
            }, status=status.HTTP_200_OK)
        
    def post(self, request, course_id):
        data = request.data
        student_id = data.get('student_id')
        date = data.get('date')
        statuss = data.get('status')

        
        # Kiểm tra xem tất cả các trường đã được gửi hay chưa
        if not all([course_id, student_id, date]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student_id = int(student_id)
            date = datetime.strptime(date, '%Y-%m-%d').date() 
        except ValueError:
            return Response(
                {"error": "'student_id' must be an integer and 'date' must be in 'YYYY-MM-DD' format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            attendance, created = Attendance.objects.get_or_create(
                course_id=course_id, student_id=student_id, date=date
            )
            attendance.status = statuss
            attendance.save()

            # Trả về phản hồi thành công
            return Response({"message": "Attendance saved successfully."}, status=status.HTTP_200_OK)
        except Exception:
            # Nếu có lỗi xảy ra khi lưu dữ liệu
            return Response({"error": "lõi"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
                "class_dates": [date for date in all_class_dates]
            })
        
        except Course.DoesNotExist:
            return Response({"detail": "Khóa học không tồn tại."})