# models.py
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from django.utils import timezone 
from django.utils.timezone import now
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Sum, Count
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.core.exceptions import ValidationError


class User(AbstractUser):
    id = models.AutoField(primary_key=True)  
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
    
    is_studying = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=LEVELS, default='none')
    has_taken_test = models.BooleanField(default=False)  


    def __str__(self):
        return f"Student: {self.user.username} - Level: {self.level}"
    
    def __str__(self):
        return f"Student: {self.user.username}"
    
    def __str__(self):
        return f"Student: {self.user.username} - Level: {self.level}"

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
    price = models.DecimalField(max_digits=10, decimal_places= 2)
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
        return current_date - datetime.timedelta(days=1)
    
    def calculate_class_dates(self):
        """
        Tính toán tất cả các ngày học cho khóa học
        :return: Danh sách các ngày học
        """
        all_class_dates = []
        num_schedules = len(self.schedules.all())
        
        # Sắp xếp các lịch học theo thứ tự
        week_days_sorted = sorted(self.schedules.all(), key=lambda x: x.weekday)
        
        current_date = self.start_date
        current_schedule_index = 0

        for _ in range(self.total_session):
            schedule = week_days_sorted[current_schedule_index]
            while current_date.weekday() != schedule.weekday:
                current_date += timedelta(days=1)
            all_class_dates.append(current_date)
            current_schedule_index = (current_schedule_index + 1) % num_schedules
            current_date += timedelta(days=1)
        
        all_class_dates.sort()
        return all_class_dates
    
    def __str__(self):
        return f"{self.name} - {self.get_level_display()}"

    def __str__(self):
        return f"{self.name} - {self.get_level_display()}"
    
    def calculate_revenue(self):
        student_count = self.students.count()
        return student_count * self.price

    def enrollment_count(self):
        return self.students.count()

    def __str__(self):
        return f"{self.name} - {self.get_level_display()}"

class StudySession(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"

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
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE, related_name='course_schedules', default=1)

    class Meta:
        unique_together = ('course', 'weekday', 'session')
        ordering = ['weekday']

    def clean(self):
        teacher = self.course.teacher
        if teacher:
            conflicts = CourseSchedule.objects.filter(
                weekday=self.weekday,
                session=self.session,
                course__teacher=teacher 
            ).exclude(pk=self.pk) 

            if conflicts.exists():
                conflict_courses = ', '.join([conf.course.name for conf in conflicts])
                raise ValidationError(
                    f"Giáo viên {teacher} đã dạy các khóa học sau trong cùng thời gian: {conflict_courses}"
                )
    def __str__(self):
        return f"{self.course.name} - {self.get_weekday_display()} {self.session}"
    
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
    LEVELS = (
        ('a1', 'A1'),
        ('a2', 'A2'),
        ('b1', 'B1'),
        ('b2', 'B2')
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='final_exams')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Thời gian làm bài (phút)")
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=2, choices=LEVELS)


    def __str__(self):
        return self.title

class Question(models.Model):
    LEVEL_CHOICES = [
        ('a1', 'A1'),
        ('a2', 'A2'),
        ('b1', 'B1'),
        ('b2', 'B2')
    ]

    EXAM_TYPE_CHOICES = [
        ('final', 'Final Exam'),
        ('placement', 'Placement Test')
    ]

    placement_test = models.ForeignKey(PlacementTest, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    final_exam = models.ForeignKey('FinalExam', on_delete=models.CASCADE, related_name='questions', null=True, blank=True)  
    text = models.TextField()
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    choice_a = models.TextField(max_length=200, default=" ", blank=True, null=True)
    choice_b = models.CharField(max_length=200, default=" " ,blank=True, null=True)
    choice_c = models.TextField(max_length=200, default=" " ,blank=True, null=True)
    choice_d = models.TextField(max_length=200, default=" ", blank=True, null=True)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], null=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.text} ({self.level})"


class Answer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='answers', null = True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    selected_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')] , null = True,) 
    is_correct = models.BooleanField(default=False) 
    exam_type = models.CharField(max_length=10, choices=[('final', 'Final Exam'), ('placement', 'Placement Test')], default='placement')
    
    def __str__(self):
        return f"{self.student.user.username} - {self.question.text} - {self.selected_answer}"

class TestResult(models.Model):
    TEST_TYPES = [
        ('placement', 'Placement Test'),
        ('final', 'Final Exam')
    ]
    
    LEVELS = [
        ('a1', 'A1'),
        ('a2', 'A2'),
        ('b1', 'B1'),
        ('b2', 'B2')
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='test_results')
    test_type = models.CharField(max_length=10, choices=TEST_TYPES)
    score = models.FloatField()
    level = models.CharField(max_length=2, choices=LEVELS)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.test_type} - {self.score}% - {self.level}"    
class Attendance(models.Model):
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        unique_together = ['course', 'student', 'date']
        ordering = ['date', 'course', 'student']

    def __str__(self):
        return f"{self.student} - {self.course.name} -  {self.status} ({self.date})"
    
    def calculate_completion(student, course):
        total_sessions = course.total_session
        if total_sessions == 0:
            return 0
        attendances = Attendance.objects.filter(
        student=student, course=course).filter(Q(status="x") | Q(status="cp")).count()

        completion_percentage = (attendances / total_sessions) * 100
        return completion_percentage
    
class Notification(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notifications')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE) 
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Notification for {self.course.name} by {self.teacher.user.username} at {self.timestamp}"
    
class Revenue(models.Model):
    date = models.DateField(default=timezone.now)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Revenue for {self.course.name} on {self.date}"

    @classmethod
    def update_revenue(cls):
        today = timezone.now().date()
        courses = Course.objects.all()
        
        for course in courses:
            student_count = CourseEnrollment.objects.filter(course=course).count()
            total_revenue = student_count * course.price
            cls.objects.update_or_create(
                date=today, 
                course=course, 
                defaults={'total_revenue': total_revenue},
            )
            
class Statistics(models.Model):
    STATISTICS_TYPES = [
        ('revenue', 'Revenue'),          
        ('student', 'Student'),        
        ('teacher', 'Teacher'),          
        ('course', 'Course'),         
    ]

    date = models.DateField(default=now)  
    type = models.CharField(max_length=50, choices=STATISTICS_TYPES) 
    data = models.JSONField()  

    class Meta:
        unique_together = ('date', 'type')  
        ordering = ['-date', 'type']

    def __str__(self):
        return f"{self.get_type_display()} Statistics for {self.date}"
    
    
