from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def principal_home(request):
    return render(request, 'principal/principal_home.html')

@login_required(login_url='/')
def add_student(request):
    return render(request,'principal/add_student.html')