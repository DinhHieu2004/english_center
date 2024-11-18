from django.urls import path
from .views import LoginView,RegisterTeacher, RegisterStudent

urlpatterns = [
    path('register/student/', RegisterStudent.as_view(), name='register_student'),
    path('login/', LoginView.as_view(), name='login'),
    path('create/teacher/', RegisterTeacher.as_view(), name='create_teacher'),  
]