from rest_framework import status
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from ..serializers import UserSerializer, StudentSerializer, TeacherSerializer, User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from ..models import Student, Teacher
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from ..serializers import PasswordResetRequestSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import HttpResponse


class LoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            if user.is_superuser:
                user_type = 'admin'
            elif user.is_student and not user.is_teacher:
                user_type = 'student'
            elif user.is_teacher and not user.is_student:
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

class LogoutView(APIView):
   permission_classes = [IsAuthenticated]

   def post(self, request):
      try:
         request.user.auth_token.delete()
         return Response ({'message ': 'logout is suscese'})
      except Exception as e :
         return Response (status= status.HTTP_400_BAD_REQUEST)

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

"""
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

"""
class PasswordResetRequestView(APIView):
    permission_classes =[AllowAny]
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            # Tạo token và uid
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Tạo link reset mật khẩu
            reset_link = f"//http://127.0.0.1:8000/api/password-reset-confirm/{uid}/{token}/"

            # Gửi email
            send_mail(
                subject="Đặt lại mật khẩu",
                message=f"Nhấn vào đây để đặt lại mật khẩu: {reset_link}",
                from_email= "22130082",
                recipient_list=[email],
            )
            return Response({"message": "Link reset mật khẩu đã được gửi đến email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def password_reset_form(request, uidb64, token):
    if request.method == 'GET':
        return render(request, 'admin/my_app/reset-password/reset_pass.html')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return render(request, 'admin/my_app/reset-password/reset_pass.html', {
                'error_message': "Mật khẩu không khớp. Vui lòng thử lại."
            })

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return HttpResponse("Liên kết không hợp lệ.", status=400)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return HttpResponse("Token không hợp lệ hoặc đã hết hạn.", status=400)

        user.set_password(new_password)
        user.save()
        return HttpResponse("Mật khẩu đã được thay đổi thành công.")