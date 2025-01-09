from collections import defaultdict
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import TeacherSerializer, CourseSerialozer, CourseScheduleSerializer, StudySessionSerializer, DiscountSerializer
from ..models import Course, Teacher, CourseSchedule, StudySession, Discount
from rest_framework.exceptions import NotFound
from rest_framework import status
from datetime import timedelta
from rest_framework.permissions import AllowAny

class CoursesDiscount(APIView):
    permission_classes = [AllowAny] 
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        discounts = Discount.objects.filter(end_date__gte=today)
        result = []
        
        for discount in discounts:
            courses = discount.courses.all()[:3]
            course_serializer = CourseSerialozer(courses, many=True)
            discount_serializer = DiscountSerializer(discount)
            result.append({
                'discount': discount_serializer.data,
                'courses': course_serializer.data
            })
        
        return Response(result, status=status.HTTP_200_OK)