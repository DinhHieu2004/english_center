from rest_framework import serializers
from .models import User, Student, Teacher
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        # Kiểm tra thông tin người dùng và mật khẩu
        user = authenticate(username=data['username'], password=data['password'])
        
        if user is None:
            raise serializers.ValidationError("Thông tin đăng nhập không chính xác")
        
        # Trả về user sau khi xác thực
        data['user'] = user
        return data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'fullname', 'is_student', 'is_teacher')
        read_only_fields = ('id', 'is_student', 'is_teacher')
class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'fullname',
                 'phone', 'address', 'date_of_birth')
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Tên người dùng này đã tồn tại")
        return value

    def create(self, validated_data):
        # Tạo user mới
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            fullname=validated_data['fullname'],
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', ''),
            date_of_birth=validated_data.get('date_of_birth'),
            is_student=True,
            is_teacher=False
        )
        
        user.set_password(validated_data['password'])
        user.save()

        # Tạo profile Student cho user
        Student.objects.create(user=user)
        
        return user

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'fullname', 'phone', 'address', 'date_of_birth', 'password', 'password2')

    def validate_password2(self, value):
        # Lấy mật khẩu từ request.data trong context
        password = self.context['request'].data.get('password')

        # Kiểm tra xem password có được gửi đi không
        if not password:
            raise serializers.ValidationError("Mật khẩu không được bỏ trống")
        
        if password != value:
            raise serializers.ValidationError("Mật khẩu xác nhận không khớp")
        
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Tên người dùng này đã tồn tại")
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            fullname=validated_data['fullname'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            date_of_birth=validated_data['date_of_birth'],
            is_student=False,
            is_teacher=True  # Hoặc dùng is_teacher từ data nếu cần
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class CreateTeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    education_level = serializers.ChoiceField(choices=Teacher.EDUCATION_LEVELS)

    class Meta:
        model = Teacher
        fields = ('user', 'education_level')

    def create(self, validated_data):
        user_data = validated_data.pop('user')  
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True) 
        user = user_serializer.save()  
        
        teacher = Teacher.objects.create(
            user=user,
            education_level=validated_data['education_level']
        )
        return teacher