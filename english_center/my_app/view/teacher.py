from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import TeacherSerializer
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
