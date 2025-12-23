"""School_Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from LMS.views import auth_views, principal_views, teacher_views, student_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication URLs
    path('', auth_views.login, name='login'),
    path('index/', auth_views.index, name='home'),
    path('base/', auth_views.base, name='base'),
    path('doLogin/', auth_views.doLogin, name='doLogin'),
    path('doLogout/', auth_views.doLogout, name='logout'),
    path('profile/', auth_views.profile, name="profile"),
    path('profile/update/', auth_views.profile_update, name='profile_update'),

    # Principal URLs
    path('principal/home/', principal_views.principal_home, name='principal_home'),
    
    # Student Management
    path('principal/student/add/', principal_views.add_student, name='add_student'),
    path('principal/student/view/', principal_views.view_student, name='view_student'),
    path('principal/student/edit/<str:id>/', principal_views.edit_student, name='edit_student'),
    path('principal/student/update/', principal_views.update_student, name='update_student'),
    path('principal/student/delete/<str:admin>/', principal_views.delete_student, name='delete_student'),
    
    # Course Management
    path('principal/course/add/', principal_views.add_course, name='add_course'),
    path('principal/course/view/', principal_views.view_course, name='view_course'),
    path('principal/course/edit/<str:id>/', principal_views.edit_course, name='edit_course'),
    path('principal/course/update/', principal_views.update_course, name='update_course'),
    path('principal/course/delete/<str:id>/', principal_views.delete_course, name='delete_course'),

    # Teacher Management
    path('principal/teacher/add/', principal_views.add_teacher, name='add_teacher'),
    path('principal/teacher/view/', principal_views.view_teacher, name='view_teacher'),
    path('principal/teacher/edit/<str:id>/', principal_views.edit_teacher, name='edit_teacher'),
    path('principal/teacher/delete/<str:admin>/', principal_views.delete_teacher, name='delete_teacher'),
    path('principal/teacher/send_notification/', principal_views.teacher_send_notification, name="teacher_send_notification"),
    path('principal/teacher/save_notification/', principal_views.save_teacher_notification, name='save_teacher_notification'),
    
    # Teacher URLs
    path('teacher/home/', teacher_views.teacher_home, name='teacher_home'),
    path('teacher/notifications/', teacher_views.notifications_teacher, name='notifications_teacher'),
    path('teacher/notification/mark/<str:status>/', teacher_views.status_mark, name='status_mark'),

    # Teacher Leave
    path('teacher/leave/apply/', teacher_views.teacher_leave_apply, name='teacher_leave_apply'),
    path('teacher/leave/save/', teacher_views.teacher_leave_save, name='teacher_leave_save'),

    # Teacher Attendance
    path('teacher/attendance/take/', teacher_views.teacher_take_attendance, name='teacher_take_attendance'),
    path('teacher/attendance/save/', teacher_views.teacher_save_attendance, name='teacher_save_attendance'),
    path('teacher/attendance/view/', teacher_views.teacher_view_attendance, name='teacher_view_attendance'),

    # Leave Management (Principal)
    path('principal/teacher/leave/view/', principal_views.teacher_leave_view, name='teacher_leave_view'),
    path('principal/teacher/leave/approve/<str:id>/', principal_views.teacher_leave_approve, name='teacher_leave_approve'),
    path('principal/teacher/leave/reject/<str:id>/', principal_views.teacher_leave_disapprove, name='teacher_leave_disapprove'),
    
    path('principal/student/leave/view/', principal_views.student_leave_view, name='student_leave_view'),
    path('principal/student/leave/approve/<str:id>/', principal_views.student_leave_approve, name='student_leave_approve'),
    path('principal/student/leave/reject/<str:id>/', principal_views.student_leave_disapprove, name='student_leave_disapprove'),
    
    # Student URLs
    path('student/home/', student_views.student_home, name='student_home'),
    path('student/leave/apply/', student_views.student_apply_leave, name='student_apply_leave'),
    path('student/leave/save/', student_views.student_save_leave, name='student_save_leave'),



] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
