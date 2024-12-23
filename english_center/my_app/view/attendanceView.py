from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import TeacherSerializer, CourseSerialozer, StudentSerializer, AttendanceSerializer
from ..models import Course, Teacher, Student, Attendance, CourseSchedule
from rest_framework.exceptions import NotFound
from datetime import datetime
from django.http import JsonResponse



class AttendanceList(APIView):
    def get(self, request, course_id):
        dates = request.GET.get('dates')

        dates_list = dates.split(',')

        students = Student.objects.filter(course__id=course_id)

        attendances = Attendance.objects.filter(
        course_id=course_id,
        date__in=dates_list,
        student__in=students
        )
        attendance_data = {}
        for date in dates_list:
            attendance_data[date] = [
                {
                    'studentId': attendance.student.id,
                    'status': attendance.status
                }
                for attendance in attendances.filter(date=date)
            ]
    
        return JsonResponse(attendance_data)
        
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

class CustomPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 50

class CourseScheduleListView(APIView):
    def post(self, request, course_id):
        try:

            course = Course.objects.get(id=course_id)
            all_class_dates = course.calculate_class_dates()

            if not all_class_dates:
                return Response({"error": "Khóa học chưa có lịch học."}, status=status.HTTP_400_BAD_REQUEST)
            page = request.data.get('page', 1)
            paginator = CustomPagination()
            paginated_dates = paginator.paginate_queryset(all_class_dates, request)

            total_pages = paginator.page.paginator.num_pages
            current_page = paginator.page.number

            if total_pages == 1:
                current_page = 1 

            return paginator.get_paginated_response({
                "class_dates": [date.strftime("%Y-%m-%d") for date in paginated_dates],
                "total_pages": total_pages,
                "current_page": current_page
            })

        except Course.DoesNotExist:
            return Response({"error": "Khóa học không tồn tại."}, status=404)
