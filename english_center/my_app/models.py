# models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class User(AbstractUser):
    fullname =  models.CharField(max_length=30, null = False, blank=True)
    username =  models.CharField(max_length=20, null = False, blank=True, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null =False, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    join_date = models.DateTimeField(default=timezone.now)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    groups = models.ManyToManyField(
      'auth.Group',
        related_name='custom_user_groups',  # Đặt related_name khác để tránh xung đột
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Đặt related_name khác để tránh xung đột
        blank=True,
        help_text='Specific permissions for this user.'
    )
class Student(models.Model):
    LEVELS = (
        ('none', 'Chưa xác định'),
        ('a1', 'A1'),
        ('a2', 'A2'),
        ('b1', 'B1'),
        ('b2', 'B2')
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=LEVELS, default='none')
    has_taken_test = models.BooleanField(default=False)  # Trường theo dõi việc làm bài kiểm tra đầu vào

    def __str__(self):
        return f"Student: {self.user.username}"

class Teacher(models.Model):
    EDUCATION_LEVELS = (
        ('bachelor', 'Cử nhân'),
        ('master', 'Thạc sĩ'),
        ('phd', 'Tiến sĩ')
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVELS)
    
    def __str__(self):
        return f"Teacher: {self.user.username}"
    
class Question(models.Model):
    LEVELS = (
        ('a1', 'A1'),
        ('a2', 'A2'),
        ('b1', 'B1'),
        ('b2', 'B2')
    )
    
    content = models.TextField()
    level = models.CharField(max_length=2, choices=LEVELS)
    
    def __str__(self):
        return f"Question {self.id} - Level {self.level}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Answer for {self.question.id}"

class EntranceTest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    date_taken = models.DateTimeField(auto_now_add=True)

class StudentAnswer(models.Model):
    test = models.ForeignKey(EntranceTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class Course(models.Model):
    LEVELS = (
        ('a1', 'A1'),
        ('a2', 'A2'),
        ('b1', 'B1'),
        ('b2', 'B2')
    )

    name = models.CharField(max_length=200)
    level = models.CharField(max_length=2, choices=LEVELS)
    description = models.TextField()
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField('Student', through='CourseEnrollment')
    start_date = models.DateField()
    total_session = models.IntegerField()  # Thay thế end_date bằng total_session

    def calculate_end_date(self):
        class_days = [schedule.weekday for schedule in self.schedules.all()]
        if not class_days:
            return self.start_date  # Trả về start_date nếu không có ngày học nào được xếp lịch
        
        current_date = self.start_date
        session_count = 0
        while session_count < self.total_session:
            if current_date.weekday() in class_days:
                session_count += 1
            current_date += datetime.timedelta(days=1)
        return current_date - datetime.timedelta(days=1)  # Ngày cuối cùng của buổi học

    def __str__(self):
        return f"{self.name} - {self.get_level_display()}"

class CourseSchedule(models.Model):
    WEEKDAYS = (
        (0, 'Thứ 2'),
        (1, 'Thứ 3'),
        (2, 'Thứ 4'),
        (3, 'Thứ 5'),
        (4, 'Thứ 6'),
        (5, 'Thứ 7'),
        (6, 'Chủ nhật')
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()

    class Meta:
        unique_together = ('course', 'weekday')
        ordering = ['weekday', 'start_time']

    def __str__(self):
        return f"{self.course.name} - {self.get_weekday_display()} {self.start_time}"

class CourseEnrollment(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    final_test_passed = models.BooleanField(null=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} - {self.course}"
"""
class Attendance(models.Model):
    ATTENDANCE_STATUS = (
        ('present', 'Có mặt'),
        ('absent', 'Vắng mặt'),
        ('late', 'Đi muộn')
    )
    
    session = models.ForeignKey(CourseSession, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS)
    note = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('session', 'student')
"""
class FinalTest(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    pass_score = models.IntegerField(default=80)  # Điểm đạt (%)

class FinalTestQuestion(models.Model):
    test = models.ForeignKey(FinalTest, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField()
    points = models.IntegerField(default=1)

class FinalTestAnswer(models.Model):
    question = models.ForeignKey(FinalTestQuestion, on_delete=models.CASCADE, related_name='answers')
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

class StudentFinalTest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(FinalTest, on_delete=models.CASCADE)
    score = models.IntegerField()
    passed = models.BooleanField()
    date_taken = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'test')        