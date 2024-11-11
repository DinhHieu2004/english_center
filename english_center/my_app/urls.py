from django.urls import path
from .views import LoginView,student_registration_view, CreateTeacherView

urlpatterns = [
    path('register/student/', student_registration_view, name='register_student'),
  #  path('api/create/teacher/', views.create_teacher, name='create_teacher'),
    path('login/', LoginView.as_view(), name='login'),
    path('create/teacher/', CreateTeacherView.as_view(), name='create-teacher'),

    #path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    #path('student/dashboard/', student_dashboard, name='student_dashboard'),
    #path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
]