from tkinter.messagebox import Message
from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from LMS.models import Student, Student_Leave, Teacher, Course


@login_required(login_url='/')
def student_home(request):
    teacher_count = Teacher.objects.all().count() # they will return total no of teachre, studnt ,courses
    student_count = Student.objects.all().count()
    course_count = Course.objects.all().count()

    context ={
        'teacher_count' : teacher_count,
        'student_count' : student_count,
        'course_count' : course_count
    }
    return render(request, 'student/student_home.html', context)
    


def studnet_apply_leave(request):
    # showing the leave approved rejected or pandding
    student = Student.objects.get(admin = request.user.id)
    student_leave_history = Student_Leave.objects.filter(student_id=student)
    context = {
            'student_leave_history':student_leave_history
        }
    return render (request, 'student/student_leave_apply.html', context)


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