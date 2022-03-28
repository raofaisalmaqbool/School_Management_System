from tkinter.messagebox import Message
from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, redirect

from SMS.models import Student, Student_Leave

def student_home(request):
    return render(request, 'student/student_home.html')


def studnet_apply_leave(request):
    return render (request, 'student/student_leave_apply.html')


def student_save_leave(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')             #for get the data from field
        leave_message = request.POST.get('leave_message')       

        student_id = Student.objects.get(admin = request.user.id) # for get the id of loged in user

        student_leave = Student_Leave(               # for store the getted data into the database
            student_id = student_id,
            data = leave_date,
            message = leave_message,
        )
        student_leave.save()           # for save the getted data into the database
        messages.success(request, 'Your Leave Submited Successful')
        
        return redirect('studnet_apply_leave')