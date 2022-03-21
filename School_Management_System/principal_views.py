from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from SMS.models import Course, Session_Year 

@login_required(login_url='/')
def principal_home(request):
    return render(request, 'principal/principal_home.html')

@login_required(login_url='/')
def add_student(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    context = {
        'course' : course,
        'session_year' : session_year,

    }
    return render(request,'principal/add_student.html', context)