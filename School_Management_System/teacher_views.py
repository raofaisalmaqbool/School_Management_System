from django.shortcuts import render, redirect
from SMS.models import Teacher, Teacher_Notification

def teacher_home(request):
    return render(request, 'teacher/teacher_home.html')

def notifications_tec(request):
    return render(request, 'teacher/teacher_notification.html')