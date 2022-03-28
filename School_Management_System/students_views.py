from django.shortcuts import render, redirect

def student_home(request):
    return render(request, 'student/student_home.html')


def studnet_apply_leave(request):
    return render (request, 'student/student_leave_apply.html')


def student_save_leave(request):
    return None