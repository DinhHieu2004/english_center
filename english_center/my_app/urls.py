from django.urls import path
from .view.authViews import LoginView,RegisterTeacher, RegisterStudent
from  .view.examViews import PlacementTestView

urlpatterns = [
    path('register/student/', RegisterStudent.as_view(), name='register_student'),
    path('login/', LoginView.as_view(), name='login'),
    path('create/teacher/', RegisterTeacher.as_view(), name='create_teacher'),  
    path('placement-test/', PlacementTestView.as_view(), name='placement-test'),  

]