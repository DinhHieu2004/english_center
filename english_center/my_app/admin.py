from django.contrib import admin
from django import forms
from .models import User, Question, FinalExam, PlacementTest, Student, Teacher,Course, CourseEnrollment, CourseSchedule, TestResult, Answer, TestResult, Attendance
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from django.contrib import messages
 #from django.core.exceptions import ValidationError

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student Information'

class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'Teacher Information'

class CustomUserAdmin(UserAdmin):
    list_display = ('id','username', 'fullname', 'email', 'phone', 'is_student', 'is_teacher', 
                   'is_active', 'is_staff', 'join_date')
    
    list_filter = ('is_student', 'is_teacher', 'is_staff', 'is_active', 'join_date')
    
    search_fields = ('username', 'fullname', 'email', 'phone')
    
    ordering = ('-join_date',)

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Information', {
            'fields': ('fullname', 'email', 'phone', 'address', 'date_of_birth')
        }),
        ('Roles', {
            'fields': ('is_student', 'is_teacher')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('join_date', 'last_login')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'fields': ('fullname', 'email', 'phone', 'address', 'date_of_birth'),
        }),
        ('Roles', {
            'fields': ('is_student', 'is_teacher', 'is_staff', 'is_active'),
        }),
    )

    inlines = [StudentInline, TeacherInline]
    
    def save_model(self, request, obj, form, change):
        if not change or (change and form.cleaned_data.get('password1')):
            password = form.cleaned_data.get('password1')
            if password:
                obj.password = make_password(password)
        
        super().save_model(request, obj, form, change)

    actions = ['make_student', 'make_teacher', 'make_active', 'make_inactive']
    
    def make_student(self, request, queryset):
        queryset.update(is_student=True, is_teacher=False)
        for user in queryset:
            Student.objects.get_or_create(user=user)
    make_student.short_description = "Mark selected users as students"
    
    def make_teacher(self, request, queryset):
        queryset.update(is_teacher=True, is_student=False)
        for user in queryset:
            Teacher.objects.get_or_create(user=user)
    make_teacher.short_description = "Mark selected users as teachers"
    
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected users as active"
    
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected users as inactive"

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'level', 'has_taken_test')
    list_filter = ('level', 'has_taken_test','is_studying')
    search_fields = ('user__username', 'user__fullname')

 
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'education_level')
    list_filter = ('education_level',)
    search_fields = ('user__username', 'user__fullname')

admin.site.register(User, CustomUserAdmin)

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ('text', 'audio_file', 'choice_a', 'choice_b', 'choice_c', 'choice_d', 'correct_answer', 'level')

@admin.register(FinalExam) 
class FinalExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]

@admin.register(PlacementTest)

class PlacementTestAdmin(admin.ModelAdmin):
    list_display =('title', 'duration', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    inlines = [QuestionInline]



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'level', 'final_exam', 'placement_test', 'correct_answer')
    list_filter = ('level', 'final_exam', 'placement_test')
    search_fields = ('text', 'choice_a', 'choice_b', 'choice_c', 'choice_d')
    
    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Question Text'

    fieldsets = (
        ('Question Content', {
            'fields': ('text', 'audio_file')
        }),
        ('Choices', {
            'fields': ('choice_a', 'choice_b', 'choice_c', 'choice_d', 'correct_answer')
        }),
        ('Classification', {
            'fields': ('level', 'final_exam', 'placement_test')
        })
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'question_preview', 'selected_answer', 'is_correct', 'exam_type')
    list_filter = ('is_correct', 'exam_type', 'student')
    search_fields = ('student__user__username', 'question__text')
    
    def question_preview(self, obj):
        return obj.question.text[:50] + "..." if len(obj.question.text) > 50 else obj.question.text
    question_preview.short_description = 'Question'



# course
class CourseScheduleInline(admin.TabularInline):
    model = CourseSchedule
    extra = 1 
    fields = ('weekday', 'start_time')

class CourseEnrollmentInline(admin.TabularInline):
    model = CourseEnrollment
    extra = 0
    readonly_fields = ('enrollment_date',)
    fields = ('student', 'completed', 'final_test_passed')

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    fields = ('student', 'date', 'status')
    show_change_link = True
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        course_id = request.resolver_match.kwargs.get('object_id')
        
        if course_id:
            if db_field.name == 'student':
                kwargs['queryset'] = Student.objects.filter(courseenrollment__course_id=course_id)
        
            elif db_field.name == 'date':
                try:
                    course = Course.objects.get(id=course_id)
                except Course.DoesNotExist:
                    course = None
            
                if course:
                    valid_dates = course.calculate_class_dates()
                    valid_dates_display = [date.strftime("%Y-%m-%d") for date in valid_dates]
                    kwargs['widget'] = forms.Select(choices=[(date, date) for date in valid_dates_display])

        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_queryset(self, request):
        course_id = request.resolver_match.kwargs.get('object_id')
        if course_id:
            return Attendance.objects.filter(course_id=course_id)
        return Attendance.objects.all()


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level', 'teacher', 'price','start_date', 'total_session')
    list_filter = ('level', 'teacher',)
    search_fields = ('name',)
    inlines = [CourseScheduleInline, CourseEnrollmentInline, AttendanceInline]
    
    fieldsets = (
        ('Thông tin khóa học', {
            'fields': ('name', 'level', 'description','price', 'teacher')
        }),
        ('Chi tiết khóa học', {
            'fields': ('start_date', 'total_session')
        })
    )

@admin.register(CourseSchedule)
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'weekday', 'start_time')
    list_filter = ('course', 'weekday')

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'completed', 'final_test_passed')
    list_filter = ('course', 'completed', 'final_test_passed')
    search_fields = ('student__user__username', 'course__name')

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display =('student','test_type', 'score',  'level','total_questions','correct_answers')    

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'course', 'date') 
    search_fields = ('student__name', 'course__name')
    list_editable = ('status',) 
    list_per_page = 20 
    ordering = ('-date',) 
    