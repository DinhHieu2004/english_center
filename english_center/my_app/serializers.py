from rest_framework import serializers
from .models import User, Student, Teacher, Course, CourseSchedule, Question, PlacementTest, FinalExam, Notification,  Attendance, StudySession
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator



class NotificationSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.username', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'course_name', 'teacher_name', 'timestamp']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        
        if user is None:
            raise serializers.ValidationError("Thông tin đăng nhập không chính xác")
        
        data['user'] = user
        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'fullname', 'phone', 'address', 'email', 'date_of_birth', 'is_student', 'is_teacher','join_date']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  #
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  
        instance.save()
        return instance
    

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [ 'level','has_taken_test']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['education_level']
class StudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySession
        fields = ['id','name', 'start_time', 'end_time']

class CourseScheduleSerializer(serializers.ModelSerializer):
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    session = serializers.StringRelatedField()
    
    class Meta:
        model = CourseSchedule
        fields = ['weekday_display', 'session']    

class CourseSerialozer(serializers.ModelSerializer):
    schedules = CourseScheduleSerializer(many = True)
    class Meta:
        model = Course
        fields = ['id','name', 'level', 'description','price', 'teacher', 'start_date', 'total_session', 'schedules']


#
class QuestionSerializer(serializers.ModelSerializer):
    audio_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'audio_file_url', 'choice_a', 'choice_b', 'choice_c', 'choice_d']

    def get_audio_file_url(self, obj):
        if obj.audio_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.audio_file.url.strip('/'))
            return obj.audio_file.url
        return None
#
class PlacementTestSerializer(serializers.ModelSerializer):
    questions  = QuestionSerializer(many = True, read_only = True)

    class Meta:
        model = PlacementTest
        fields = ['id', 'title', 'description', 'duration', 'questions']


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_id = serializers.IntegerField(source='course.id', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student_name', 'course_id', 'status', 'date',]
    
        def create(self, validated_data):
            validated_data['status'] = validated_data.get('status', None)
            return super().create(validated_data)

        def update(self, instance, validated_data):
            status = validated_data.get('status', None)
            if status is None:
                instance.status = None  
            else:
                instance.status = status
            return super().update(instance, validated_data)        
        
#reset-password
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not exits.")
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError("Invalid UID")

        if not PasswordResetTokenGenerator().check_token(user, data['token']):
            raise serializers.ValidationError("Token invalid.")

        return data

    def save(self):
        uid = force_str(urlsafe_base64_decode(self.validated_data['uid']))
        user = User.objects.get(pk=uid)
        user.set_password(self.validated_data['new_password'])
        user.save()
