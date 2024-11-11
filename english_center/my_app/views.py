from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .serializers import StudentRegistrationSerializer, CreateTeacherSerializer
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import User, Teacher



@api_view(['POST'])
@permission_classes([AllowAny])
def student_registration_view(request):
    if request.method == 'POST':
        serializer = StudentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Đăng ký tài khoản thành công",
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "fullname": user.fullname
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
    
        if user is not None:
          # Xác định user type
           if user.is_superuser:
            user_type = 'admin'
           elif hasattr(user, 'student'):
            user_type = 'student'
           elif hasattr(user, 'teacher'):
            user_type = 'teacher'
           else:
            user_type = 'unknown'
            
           return Response({
            'message': 'Login successful',
            'user_type': user_type
              })
        else:
           return Response({
              'message': 'Invalid credentials'
           }, status=status.HTTP_401_UNAUTHORIZED)
 
class CreateTeacherView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateTeacherSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            teacher = serializer.save()
            return Response({"message": "Teacher created successfully", "teacher_id": teacher.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)