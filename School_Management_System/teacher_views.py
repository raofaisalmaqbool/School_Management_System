from django.shortcuts import render, redirect

def teacher_home(request):
    return render(request, 'teacher/teacher_home.html')