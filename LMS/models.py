from django.db import models
from django.contrib.auth.models import AbstractUser


class Class(models.Model):
    """
    Model representing a class/grade level in the school.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return self.name

class Customuser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Supports three types of users: Principal, Teachers, and Students.
    """
    USER_TYPE_CHOICES = (
        ('1', 'PRINCIPAL'),
        ('2', 'TEACHER'),
        ('3', 'STUDENT'),
    )

    user_type = models.CharField(
        choices=USER_TYPE_CHOICES,
        max_length=50,
        default='1'
    )
    profile_pic = models.ImageField(
        upload_to='profile_pics',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Teacher(models.Model):
    """
    Model representing a teacher in the school.
    Linked to Customuser with user_type='2'.
    """
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    admin = models.OneToOneField(Customuser, on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"

class Course(models.Model):
    """
    Model representing a course/subject taught in the school.
    """
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    name = models.CharField(max_length=80, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.name
    
class Session_Year(models.Model):
    """
    Model representing an academic session/year.
    """
    session_start = models.CharField(max_length=80)
    session_end = models.CharField(max_length=80)

    class Meta:
        verbose_name = 'Session Year'
        verbose_name_plural = 'Session Years'

    def __str__(self):
        return f"{self.session_start} To {self.session_end}"


class Student(models.Model):
    """
    Model representing a student in the school.
    Linked to Customuser with user_type='3'.
    """
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    admin = models.OneToOneField(Customuser, on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    course_id = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        related_name='students'
    )
    session_year_id = models.ForeignKey(
        Session_Year,
        on_delete=models.SET_NULL,
        null=True,
        related_name='students'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"



class Teacher_Notification(models.Model):
    """
    Model for notifications sent to teachers.
    Status: 0=Unread, 1=Read
    """
    teacher_id = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Teacher Notification'
        verbose_name_plural = 'Teacher Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.teacher_id.admin.first_name}"


class Teacher_leave(models.Model):
    """
    Model for teacher leave applications.
    Status: 0=Pending, 1=Approved, 2=Rejected
    """
    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Rejected'),
    )

    teacher_id = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='leave_applications'
    )
    date = models.DateField()
    message = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Teacher Leave'
        verbose_name_plural = 'Teacher Leaves'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.teacher_id.admin.first_name} {self.teacher_id.admin.last_name} - {self.date}"


class Student_Leave(models.Model):
    """
    Model for student leave applications.
    Status: 0=Pending, 1=Approved, 2=Rejected
    """
    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Rejected'),
    )

    student_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='leave_applications'
    )
    date = models.DateField()
    message = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student Leave'
        verbose_name_plural = 'Student Leaves'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student_id.admin.first_name} {self.student_id.admin.last_name} - {self.date}"


class Attendance(models.Model):
    """
    Model representing an attendance record for a specific course and date.
    """
    course_id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(
        Session_Year,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        unique_together = ('course_id', 'attendance_date', 'session_year_id')

    def __str__(self):
        return f"{self.course_id.name} - {self.attendance_date}"

class Attendance_Report(models.Model):
    """
    Model representing individual student attendance for a specific attendance record.
    Only present students are recorded.
    """
    student_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_reports'
    )
    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Attendance Report'
        verbose_name_plural = 'Attendance Reports'
        unique_together = ('student_id', 'attendance')

    def __str__(self):
        return f"{self.student_id.admin.first_name} - {self.attendance.attendance_date}"


class Student_Result(models.Model):
    """
    Model representing student exam results for a specific course.
    """
    student_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='results'
    )
    course_id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='results'
    )
    assignment_marks = models.IntegerField(default=0)
    presentation_marks = models.IntegerField(default=0)
    exam_marks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student Result'
        verbose_name_plural = 'Student Results'
        unique_together = ('student_id', 'course_id')

    @property
    def total_marks(self):
        """Calculate total marks."""
        return self.assignment_marks + self.presentation_marks + self.exam_marks

    def __str__(self):
        return f"{self.student_id.admin.first_name} - {self.course_id.name}"