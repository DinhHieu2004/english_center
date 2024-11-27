from rest_framework import status
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from ..serializers import UserSerializer, StudentSerializer, TeacherSerializer
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from ..models import Student, Teacher


class LoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
           token, _ = Token.objects.get_or_create(user=user)
          # Xác định user type
           if user.is_superuser:
            user_type = 'admin'
           elif hasattr(user, 'student'):
            user_type = 'student'
           elif hasattr(user, 'teacher'):
            user_type = 'teacher'
           else:
            user_type = 'unknown'
            
           user_data = UserSerializer(user).data
           if user_type == 'student':
                student_data = StudentSerializer(user.student).data
                user_data['student_details'] = student_data
           elif user_type == 'teacher':
                teacher_data = TeacherSerializer(user.teacher).data
                user_data['teacher_details'] = teacher_data

           return Response({
                'message': 'Login successful',
                'token': token.key, 
                'user_type': user_type,
                'user_data': user_data
            })
        else:
            return Response({
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class RegisterStudent(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        user_data = request.data.get('user')
        student_data = request.data.get('student', {})

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(is_student=True, is_teacher=False)  

            student_data['level'] = 'none'  
            student_serializer = StudentSerializer(data=student_data)
            if student_serializer.is_valid():
                student = student_serializer.save(user=user)
                return Response({'message': 'Student registered successfully!'}, status=status.HTTP_201_CREATED)
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
   permission_classes = [IsAuthenticated]
   
   def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        cf_new_password = request.data.get('cf_new_password')

        if not user.check_password(current_password):
           return Response({'message': 'current pass is not incorrect'},
                           status= status.HTTP_400_BAD_REQUEST)
        if len(new_password) < 8 :
           return Response ({'message ': 'new password must at least 8 characters long'},
                            status= status.HTTP_400_BAD_REQUEST)
        if new_password != cf_new_password :
           return Response ({'message ': 'new password and confirm new password must be sample'},
                            status= status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed succsessfuly'}, status= status.HTTP_200_OK)

class RegisterTeacher(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        user_data = request.data.get('user')
        teacher_data = request.data.get('teacher', {})

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(is_student=False, is_teacher=True)  

            teacher_serializer = TeacherSerializer(data=teacher_data)
            if teacher_serializer.is_valid():
                teacher = teacher_serializer.save(user=user)
                return Response({'message': 'Teacher registered successfully!'}, status=status.HTTP_201_CREATED)
            return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




