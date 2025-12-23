"""
Django forms for the LMS application.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customuser, Student, Teacher, Course


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new users with custom fields.
    """
    class Meta:
        model = Customuser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'profile_pic')


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating user information.
    """
    class Meta:
        model = Customuser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_pic')


class StudentForm(forms.ModelForm):
    """
    Form for creating and updating student records.
    """
    class Meta:
        model = Student
        fields = ['address', 'gender', 'course_id', 'session_year_id']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'course_id': forms.Select(attrs={'class': 'form-control'}),
            'session_year_id': forms.Select(attrs={'class': 'form-control'}),
        }


class TeacherForm(forms.ModelForm):
    """
    Form for creating and updating teacher records.
    """
    class Meta:
        model = Teacher
        fields = ['address', 'gender']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }


class CourseForm(forms.ModelForm):
    """
    Form for creating and updating courses.
    """
    class Meta:
        model = Course
        fields = ['name', 'teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }