from collections import defaultdict
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import TeacherSerializer, CourseSerialozer, CourseScheduleSerializer, StudySessionSerializer
from ..models import Course, Teacher, CourseSchedule, StudySession
from rest_framework.exceptions import NotFound
from rest_framework import status
from datetime import timedelta

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

    def get_teacher_schedule(self, teacher_id, start_date, end_date):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return None
        
        courses = teacher.course_set.all()
        sessions = StudySession.objects.all()
        serializer = StudySessionSerializer(sessions, many=True) 
        num_session = sessions.count()

        schedule = defaultdict(lambda: {i: None for i in range(1, num_session+ 1)})
        
        for course in courses:
            for schedule_item in course.schedules.all().order_by('session'):
                class_dates = course.calculate_class_dates()
                for class_date in class_dates:
                    start_date_date = start_date.date()
                    end_date_date = end_date.date()   
                    
                    if start_date_date <= class_date <= end_date_date and class_date.weekday() == schedule_item.weekday:
                        session_str = str(schedule_item.session) if schedule_item.session else "No session assigned"
                        
                        schedule[class_date.weekday() + 1][schedule_item.session_id] = {
                            'course_name': course.name,
                            'start_time': session_str,
                            'class_date': class_date
                        }

        return {
        'teacher_schedule': schedule,
        'all_sessions': serializer.data
    }

    def get(self, request, teacher_id):
        week_start_str = request.query_params.get('start_date')
        week_end_str = request.query_params.get('end_date')

        if not week_start_str or not week_end_str:
            return Response({'error': 'Missing start_date or end_date in query parameters'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.datetime.strptime(week_start_str, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(week_end_str, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Invalid date format. Expected format: YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        teacher_schedule = self.get_teacher_schedule(teacher_id, start_date, end_date)
        
        if teacher_schedule is None:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(teacher_schedule, status=status.HTTP_200_OK)