from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import TeacherSerializer, CourseSerialozer
from ..models import Course, Teacher
from rest_framework.exceptions import NotFound

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
        courses = Course.objects.filter(teacher = teacher)
        courses_data= CourseSerialozer(courses, many = True).data
        return Response({'courses_data': courses_data})