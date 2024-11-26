from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import StudentSerializer, CourseSerialozer
from ..models import Course
from rest_framework.exceptions import NotFound


class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'student'):
            return Response({'error': 'user is not student'}, status= 400)
        
        student = user.student
        current_course = Course.objects.filter(students = student)
        if current_course.exists():
            course_data= CourseSerialozer(current_course, many = True).data
            return Response({
                'current_data': course_data,
                'available_cources': []
            })
        else:
            next_level_courses = Course.objects.filter(level = self.get_next_level(student.level))
            available_courses =CourseSerialozer(next_level_courses, many =True).data
            return Response({
                'current_courses': [],
                'avilable_courses': available_courses
            })
        
    def get_next_level(self, current_level):
        levels = ['none', 'a1', 'a2', 'b1', 'b2']
        try:
            current_index = levels.index(current_level)
            return levels[current_index + 1] if current_index + 1 < len(levels) else None
        except ValueError:
            return None    
        
class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try: 
            course = Course.objects.get(id = id)
        except Course.DoesNotExist:
            raise NotFound(detail="Course not found")

        course_data =CourseSerialozer(course).data
        return Response({'course': course_data}, status= 200)            

class TeacherDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user     
        teacher = user.teacher
        courses = Course.objects.filter(teacher = teacher)
        courses_data= CourseSerialozer(courses, many = True).data
        return Response({'courses_data': courses_data})