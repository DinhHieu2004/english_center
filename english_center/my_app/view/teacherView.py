from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import TeacherSerializer, CourseSerialozer, CourseScheduleSerializer
from ..models import Course, Teacher, CourseSchedule
from rest_framework.exceptions import NotFound
from rest_framework import status

# views.py
class TeacherView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            teacher = Teacher.objects.get(id=id)
        except Teacher.DoesNotExist:
            raise NotFound(detail="Teacher not found")

        teacher_name = teacher.user.fullname
        
        return Response({'teacher_name': teacher_name})

class TeacherDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user     
        teacher = user.teacher
        courses = Course.objects.filter(teacher=teacher)
        courses_data = CourseSerialozer(courses, many=True).data
        response_data = {
            'teacher_id': teacher.id,
            'courses_data': courses_data
        }

        return Response(response_data)
    
class TeacherScheduleView(APIView):
    serializer_class = CourseScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_teacher_schedule(self, teacher_id):
        """
        Hàm tính toán lịch học của giáo viên
        """
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return None
        
        courses = teacher.course_set.all()
        schedule = defaultdict(list)

        for course in courses:
            for schedule_item in course.schedules.all():
                class_dates = course.calculate_class_dates()
                for class_date in class_dates:
                    if class_date.weekday() == schedule_item.weekday:
                        session_str = str(schedule_item.session) if schedule_item.session else "No session assigned"
                        schedule[schedule_item.get_weekday_display()].append({
                            'course_name': course.name,
                            'start_time': session_str,
                            'class_date': class_date
                    })

        # Sắp xếp lịch học theo giờ
        for weekday in schedule:
            schedule[weekday].sort(key=lambda x: x['start_time'])
        
        return schedule

    def get(self, request, teacher_id):
        """
        API Endpoint trả về lịch dạy của giáo viên
        """
        teacher_schedule = self.get_teacher_schedule(teacher_id)
        
        if teacher_schedule is None:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(teacher_schedule, status=status.HTTP_200_OK)