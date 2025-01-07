
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import StudentSerializer, CourseSerialozer
from ..models import Course, Student, CourseEnrollment, Attendance
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.shortcuts import get_object_or_404


class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        if not hasattr(user, 'student'):
            return Response({'error': 'user is not student'}, status= status.HTTP_400_BAD_REQUEST)
        
        student = user.student
        enrolled_courses = CourseEnrollment.objects.filter(student=student, completed=False)
        current_courses = [enrollment.course for enrollment in enrolled_courses]
        if current_courses:
            current_course = current_courses[0]
            course_data = CourseSerialozer(current_course).data
            complete = Attendance.calculate_completion(student, current_course)
            return Response({
                'complete': complete,
                'current_course': course_data,
                'available_cources': []
            })
        else:
            next_level_courses = Course.objects.filter(level=student.level)
            available_courses =CourseSerialozer(next_level_courses, many =True,  context={'student': student}).data
            return Response({
                'current_courses': [],
                'available_courses': available_courses
            })
'''    
    def get_next_level(self, current_level):
        levels = ['none', 'a1', 'a2', 'b1', 'b2']
        try:
            current_index = levels.index(current_level)
            return levels[current_index + 1] if current_index + 1 < len(levels) else None
        except ValueError:
            return None    
'''
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

        return Response({'student': student_data}, status= status.HTTP_200_OK)    


class StudentEnrollmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            student = request.user.student  
            if student.is_studying:
                return Response(
                    {"error": "You must complete your current course before registering for a new one."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            course_id = request.data.get('course')
            course = get_object_or_404(Course, id=course_id)

            payment = request.data.get('payment', None)
            if not payment:
                return Response(
                    {"error": "Payment is required to register for the course."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            student.is_studying = True
            student.save()
            
            enrollment = CourseEnrollment.objects.create(student=student, course=course)

            return Response(
                {"message": "You have successfully registered for the course."},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)            