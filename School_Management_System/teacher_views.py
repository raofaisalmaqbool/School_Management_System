from django.shortcuts import render, redirect
from SMS.models import Teacher, Teacher_Notification

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


