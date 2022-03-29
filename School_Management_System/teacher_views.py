from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from SMS.models import Course, Session_Year, Student, Teacher, Teacher_Notification, Teacher_leave

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

    action = request.GET.get('action')

    get_course = None
    students = None
    get_session_year = None

    if action is not None:
        if request.method == "POST":
            course_id = request.POST.get('course_id')
            session_year_id = request.POST.get('session_id')

            get_course = Course.objects.get(id = course_id)
            get_session_year = Session_Year.objects.get(id = session_year_id)

            course = Course.objects.filter(id=course_id)
            for i in course:
                student_id = i.id
                students = Student.objects.filter(course_id=student_id)

    context ={
        'course':course,
        'session_year':session_year,
        'get_course':get_course,
        'get_session_year':get_session_year,
        'action':action,
        'students':students,
    }
    return render(request, 'teacher/take_attendance.html', context)


