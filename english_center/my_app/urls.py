from django.urls import path
from .view.authViews import LoginView,RegisterTeacher, RegisterStudent
from  .view.examViews import PlacementTestView
from  .view.course import StudentDashboardView, CourseDetailView, TeacherDashboardView
from .view.teacher import TeacherView


urlpatterns = [
    path('register/student/', RegisterStudent.as_view(), name='register_student'),
    path('login/', LoginView.as_view(), name='login'),
    path('create/teacher/', RegisterTeacher.as_view(), name='create_teacher'),  
    path('placement-test/', PlacementTestView.as_view(), name='placement-test'),  
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('course/<int:id>/', CourseDetailView.as_view(), name='course-detail'),
    path('teacher/<int:id>/', TeacherView.as_view(), name='teacher-detail'),
    path('teacher/dashboard/', TeacherDashboardView.as_view(), name='teacher_courses'),

]