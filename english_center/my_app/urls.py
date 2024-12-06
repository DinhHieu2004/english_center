from django.urls import path
from .view.authViews import LoginView, RegisterStudent, ChangePasswordView, LogoutView
from  .view.examViews import PlacementTestView
from  .view.coursevView import  CourseDetailView, CourseStudentsAPIView
from .view.teacherView import TeacherView,TeacherDashboardView
from .view.studentView import StudentDashboardView, StudentDetailView, StudentEnrollmentView


urlpatterns = [
    path('register/student/', RegisterStudent.as_view(), name='register_student'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('placement-test/', PlacementTestView.as_view(), name='placement-test'),  
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('course/<int:id>/', CourseDetailView.as_view(), name='course-detail'),
    path('teacher/<int:id>/', TeacherView.as_view(), name='teacher-detail'),
    path('teacher/dashboard/', TeacherDashboardView.as_view(), name='teacher_courses'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('student/<int:student_id>/', StudentDetailView.as_view(), name='student-detail'),
    path('course/<int:course_id>/students/', CourseStudentsAPIView.as_view(), name='course-students'),
    path('enroll-course/', StudentEnrollmentView.as_view(), name='enroll-course'),

]