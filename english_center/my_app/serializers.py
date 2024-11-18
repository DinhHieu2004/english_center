from rest_framework import serializers
from .models import User, Student, Teacher, Course, CourseSchedule
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model



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


class CourseSerialozer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'level', 'description', 'teacher', 'start_date']

class CourseScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSchedule
        fields = []      