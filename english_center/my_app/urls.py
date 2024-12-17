from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .view.authViews import LoginView, RegisterStudent, ChangePasswordView, LogoutView,PasswordResetRequestView, password_reset_form
from  .view.examViews import PlacementTestView
from  .view.coursevView import  CourseDetailView, CourseStudentsAPIView
from .view.teacherView import TeacherView,TeacherDashboardView, TeacherScheduleView
from .view.studentView import StudentDashboardView, StudentDetailView, StudentEnrollmentView
from .view.notificationView import NotificationListView
from .view.attendanceView import AttendanceList, CourseScheduleListView



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
    path('notification/<int:course_id>/', NotificationListView.as_view(), name='send-notification'),
    path('course/<int:course_id>/attendance/', AttendanceList.as_view(), name='attendance-list'),
    path('course/<int:course_id>/schedule/', CourseScheduleListView.as_view(), name='course-schedule-list'),
    path('teacher/<int:teacher_id>/schedule/', TeacherScheduleView.as_view(), name='teacher-schedule'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', password_reset_form, name='password_reset_confirm'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)