from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import StudentSerializer, CourseSerialozer, UserSerializer
from ..models import Course, Student
from rest_framework.exceptions import NotFound

class StudentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            user = student.user
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found")
        student_data = {
            'name': user.fullname,  
            'email': user.email,  
            'phone': user.phone,
            'address': user.address
        }

        # Trả về thông tin của học viên
        return Response({'student': student_data}, status=200)