import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Student, Teacher

@pytest.fixture
def api_client():
    return APIClient()

# Test đăng ký sinh viên
@pytest.mark.django_db
def test_register_student(api_client):
    # Thông tin user và student
    user_data = {
        "username": "student_user",
        "fullname": "Student Name",
        "phone": "1234567890",
        "address": "123 Street",
        "email": "student@example.com",
        "date_of_birth": "2000-01-01",
        "password": "strongpassword123"
    }
    student_data = {
        "level": "none",
        "has_taken_test": False
    }

    # Gửi POST request để đăng ký sinh viên
    response = api_client.post('/register/student/', {
        'user': user_data,
        'student': student_data
    }, format='json')

    # Kiểm tra mã trạng thái và phản hồi
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'Student registered successfully!'

    # Kiểm tra xem người dùng và sinh viên đã được tạo trong cơ sở dữ liệu
    user = get_user_model().objects.get(username=user_data['username'])
    student = Student.objects.get(user=user)
    assert student.level == 'none'
    assert student.has_taken_test is False

# Test đăng ký giáo viên
@pytest.mark.django_db
def test_register_teacher(api_client):
    # Thông tin user và teacher
    user_data = {
        "username": "teacher_user",
        "fullname": "Teacher Name",
        "phone": "0987654321",
        "address": "456 Avenue",
        "email": "teacher@example.com",
        "date_of_birth": "1980-05-05",
        "password": "teacherpassword123"
    }
    teacher_data = {
        "education_level": "master"
    }

    # Gửi POST request để đăng ký giáo viên
    response = api_client.post('/create/teacher/', {
        'user': user_data,
        'teacher': teacher_data
    }, format='json')

    # Kiểm tra mã trạng thái và phản hồi
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'Teacher registered successfully!'

    # Kiểm tra xem người dùng và giáo viên đã được tạo trong cơ sở dữ liệu
    user = get_user_model().objects.get(username=user_data['username'])
    teacher = Teacher.objects.get(user=user)
    assert teacher.education_level == 'master'

# Test đăng ký sinh viên mà không cung cấp thông tin người dùng
@pytest.mark.django_db
def test_register_student_missing_user(api_client):
    student_data = {
        "level": "none",
        "has_taken_test": False
    }

    # Gửi POST request thiếu thông tin người dùng
    response = api_client.post('/register/student/', {
        'student': student_data
    }, format='json')

    # Kiểm tra mã trạng thái lỗi và thông báo lỗi
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'user' in response.data  # Kiểm tra lỗi thiếu dữ liệu user

# Test đăng ký giáo viên mà không cung cấp thông tin người dùng
@pytest.mark.django_db
def test_register_teacher_missing_user(api_client):
    teacher_data = {
        "education_level": "master"
    }

    # Gửi POST request thiếu thông tin người dùng
    response = api_client.post('/create/teacher/', {
        'teacher': teacher_data
    }, format='json')

    # Kiểm tra mã trạng thái lỗi và thông báo lỗi
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'user' in response.data  # Kiểm tra lỗi thiếu dữ liệu user
