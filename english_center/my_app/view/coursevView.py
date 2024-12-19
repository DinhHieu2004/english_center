from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import  CourseSerialozer, StudentSerializer
from ..models import Course
from rest_framework.exceptions import NotFound


class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try: 
            course = Course.objects.get(id = id)
        except Course.DoesNotExist:
            raise NotFound(detail="Course not found")

        course_data =CourseSerialozer(course).data
        return Response({'course': course_data, }, status= 200)            

class CourseStudentsAPIView(APIView):
    def get(self, request, course_id, *args, **kwargs):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise NotFound(detail="Course not found") 

        students = course.students.all().order_by('id') 
        if not students.exists():
            return Response({"message": "No students enrolled in this course."})

        students_data = []
        for student in students:
            student_id = student.id
            user = student.user

            student_data = {
                'id': student_id,
                'name': user.fullname,
                'email': user.email,
                'phone': user.phone,
                'birth_date': user.date_of_birth,
                'address': user.address
            }
            students_data.append(student_data)

        return Response({
            'course': course.name,
            'students': students_data 
        })