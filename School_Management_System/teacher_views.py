from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from SMS.models import Course, Session_Year, Teacher, Teacher_Notification, Teacher_leave

def teacher_home(request):
    return render(request, 'teacher/teacher_home.html')

def notifications_tec(request):
    teacher = Teacher.objects.filter(admin = request.user.id)
    for i in teacher:
        teacher_id =i.id
        notifications_tec = Teacher_Notification.objects.filter(teacher_id = teacher_id)
        context ={
            'notifications_tec' : notifications_tec
        }
        return render(request, 'teacher/teacher_notification.html', context)

def status_mark(request, status):
    notification = Teacher_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('notifications_tec')


def teacher_leave_apply(request):
    teacher = Teacher.objects.filter(admin = request.user.id)
    for i in teacher:
        teacher_id = i.id
        teacher_leave_history = Teacher_leave.objects.filter(teacher_id=teacher_id)
        context = {
            'teacher_leave_history':teacher_leave_history
        }
        return render(request, 'teacher/teacher_leave_apply.html', context)

    

def teacher_leave_save(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        teacher = Teacher.objects.get(admin = request.user.id)

        leave = Teacher_leave(
            teacher_id = teacher,
            data = leave_date,
            message = leave_message,
        )
        leave.save()
        messages.success(request, 'Your Leave Submited Successful')
        
        return redirect('teacher_leave_apply')


    

def teacher_take_attendance(request):
    teacher_id = Teacher.objects.get(admin = request.user.id)
    course = Course.objects.filter(teacher = teacher_id )
    session_year = Session_Year.objects.all()

    context ={
        'course':course,
        'session_year':session_year
    }
    return render(request, 'teacher/take_attendance.html', context)


