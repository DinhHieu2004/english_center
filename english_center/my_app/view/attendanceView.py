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

        if not student or not date:
            return Response(
                {"error": "Both 'student' and 'date' parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
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
            if statuss:
                attendance, created = Attendance.objects.get_or_create(
                course_id=course_id, student_id=student_id, date=date
                )
                attendance.status = statuss
                attendance.save()
                return Response({"message": "Attendance saved successfully."}, status=status.HTTP_200_OK)
            else:
                attendance = Attendance.objects.filter(course_id=course_id, student_id=student_id, date=date)
        
                if attendance.exists():
                    attendance.delete()
                return Response({"message": "Attendance deleted successfully."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "lõi"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CourseScheduleListView(APIView):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            all_class_dates = course.calculate_class_dates()

            if not all_class_dates:
                return Response({"error": "Khóa học chưa có lịch học."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "class_dates": [date.strftime("%Y-%m-%d") for date in all_class_dates]
            })
        
        except Course.DoesNotExist:
            return Response({"error": "Khóa học không tồn tại."}, status=404)