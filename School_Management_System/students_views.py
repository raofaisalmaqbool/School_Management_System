from django.shortcuts import render, redirect

def student_home(request):
    return render(request, 'student/student_home.html')