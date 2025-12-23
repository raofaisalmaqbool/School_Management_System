from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Customuser, Course, Session_Year, Student, Teacher,
    Teacher_Notification, Teacher_leave, Student_Leave,
    Attendance, Attendance_Report, Student_Result
)


class CustomUserAdmin(UserAdmin):
    """Custom admin for user management."""
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'profile_pic')}),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin for course management."""
    list_display = ['name', 'teacher', 'created_at', 'updated_at']
    list_filter = ['teacher', 'created_at']
    search_fields = ['name', 'teacher__admin__first_name', 'teacher__admin__last_name']
    ordering = ['name']


@admin.register(Session_Year)
class SessionYearAdmin(admin.ModelAdmin):
    """Admin for session year management."""
    list_display = ['session_start', 'session_end', 'id']
    search_fields = ['session_start', 'session_end']
    ordering = ['-id']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin for student management."""
    list_display = ['get_full_name', 'get_email', 'gender', 'course_id', 'session_year_id', 'created_at']
    list_filter = ['gender', 'course_id', 'session_year_id', 'created_at']
    search_fields = ['admin__username', 'admin__email', 'admin__first_name', 'admin__last_name', 'address']
    ordering = ['-created_at']
    
    def get_full_name(self, obj):
        return f"{obj.admin.first_name} {obj.admin.last_name}"
    get_full_name.short_description = 'Name'
    
    def get_email(self, obj):
        return obj.admin.email
    get_email.short_description = 'Email'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Admin for teacher management."""
    list_display = ['get_full_name', 'get_email', 'gender', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['admin__username', 'admin__email', 'admin__first_name', 'admin__last_name', 'address']
    ordering = ['-created_at']
    
    def get_full_name(self, obj):
        return f"{obj.admin.first_name} {obj.admin.last_name}"
    get_full_name.short_description = 'Name'
    
    def get_email(self, obj):
        return obj.admin.email
    get_email.short_description = 'Email'


@admin.register(Teacher_Notification)
class TeacherNotificationAdmin(admin.ModelAdmin):
    """Admin for teacher notifications."""
    list_display = ['teacher_id', 'message_preview', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['teacher_id__admin__first_name', 'teacher_id__admin__last_name', 'message']
    ordering = ['-created_at']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'


@admin.register(Teacher_leave)
class TeacherLeaveAdmin(admin.ModelAdmin):
    """Admin for teacher leave applications."""
    list_display = ['teacher_id', 'date', 'get_status', 'created_at']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['teacher_id__admin__first_name', 'teacher_id__admin__last_name', 'message']
    ordering = ['-created_at']
    
    def get_status(self, obj):
        return obj.get_status_display()
    get_status.short_description = 'Status'


@admin.register(Student_Leave)
class StudentLeaveAdmin(admin.ModelAdmin):
    """Admin for student leave applications."""
    list_display = ['student_id', 'date', 'get_status', 'created_at']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['student_id__admin__first_name', 'student_id__admin__last_name', 'message']
    ordering = ['-created_at']
    
    def get_status(self, obj):
        return obj.get_status_display()
    get_status.short_description = 'Status'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """Admin for attendance records."""
    list_display = ['course_id', 'attendance_date', 'session_year_id', 'created_at']
    list_filter = ['course_id', 'attendance_date', 'session_year_id', 'created_at']
    search_fields = ['course_id__name']
    ordering = ['-attendance_date']


@admin.register(Attendance_Report)
class AttendanceReportAdmin(admin.ModelAdmin):
    """Admin for individual attendance reports."""
    list_display = ['student_id', 'get_course', 'get_date', 'created_at']
    list_filter = ['attendance__course_id', 'attendance__attendance_date', 'created_at']
    search_fields = ['student_id__admin__first_name', 'student_id__admin__last_name']
    ordering = ['-created_at']
    
    def get_course(self, obj):
        return obj.attendance.course_id.name
    get_course.short_description = 'Course'
    
    def get_date(self, obj):
        return obj.attendance.attendance_date
    get_date.short_description = 'Date'


@admin.register(Student_Result)
class StudentResultAdmin(admin.ModelAdmin):
    """Admin for student results."""
    list_display = ['student_id', 'course_id', 'assignment_marks', 'presentation_marks', 'exam_marks', 'get_total', 'created_at']
    list_filter = ['course_id', 'created_at']
    search_fields = ['student_id__admin__first_name', 'student_id__admin__last_name', 'course_id__name']
    ordering = ['-created_at']
    
    def get_total(self, obj):
        return obj.total_marks
    get_total.short_description = 'Total Marks'


# Register Customuser with custom admin
admin.site.register(Customuser, CustomUserAdmin)

# Customize admin site headers
admin.site.site_header = 'School Management System Admin'
admin.site.site_title = 'SMS Admin Portal'
admin.site.index_title = 'Welcome to School Management System'