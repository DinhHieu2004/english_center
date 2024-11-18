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
        related_name='custom_user_groups', 
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions', 
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
    has_taken_test = models.BooleanField(default=False)  # kiểm tra đầu vào hay chưa

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
    total_session = models.IntegerField() 

    def calculate_end_date(self):
        class_days = [schedule.weekday for schedule in self.schedules.all()]
        if not class_days:
            return self.start_date  
        
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
    
class PlacementTest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Thời gian làm bài (phút)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class FinalExam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='final_exams')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Thời gian làm bài (phút)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    LEVEL_CHOICES = [
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2')
    ]

    EXAM_TYPE_CHOICES = [
        ('final', 'Final Exam'),
        ('placement', 'Placement Test')
    ]

    placement_test = models.ForeignKey(PlacementTest, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    final_exam = models.ForeignKey('FinalExam', on_delete=models.CASCADE, related_name='questions', null=True, blank=True)  
    text = models.TextField()
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    choice_a = models.TextField(max_length=200, default=" ")
    choice_b = models.CharField(max_length=200, default=" ")
    choice_c = models.TextField(max_length=200, default=" ")
    choice_d = models.TextField(max_length=200, default=" ")
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], null=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.text} ({self.level})"

class Answer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='answers', null = True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    selected_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')] , null = True,) 
    is_correct = models.BooleanField(default=False)  # Kiểm tra đáp án đúng hay sai
    exam_type = models.CharField(max_length=10, choices=[('final', 'Final Exam'), ('placement', 'Placement Test')], default='placement')
    
    def __str__(self):
        return f"{self.student.user.username} - {self.question.text} - {self.selected_answer}"
    
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
