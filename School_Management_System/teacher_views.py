from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from SMS.models import Course, Session_Year, Student, Attendance, Attendance_Report, Teacher, Teacher_Notification, Teacher_leave

@login_required(login_url='/')
def teacher_home(request):
    teacher_count = Teacher.objects.all().count() # they will return total no of teachre, studnt ,courses
    student_count = Student.objects.all().count()
    course_count = Course.objects.all().count()

    context ={
        'teacher_count' : teacher_count,
        'student_count' : student_count,
        'course_count' : course_count
    }
    return render(request, 'teacher/teacher_home.html', context)



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



def teacher_save_attendance(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_id')
        attendance_date = request.POST.get('attendance_date')
        student_id = request.POST.getlist('student_id')

        get_course = Course.objects.get(id = course_id)
        get_session_year = Session_Year.objects.get(id = session_year_id)

        attendance = Attendance(
            course_id = get_course,
            attendance_date = attendance_date,
            session_year_id = get_session_year,
        )
        attendance.save()
        for i in student_id:
            stud_id = i
            int_stud = int(stud_id)

            p_students = Student.objects.get(id = int_stud)
            attendance_report = Attendance_Report(
                student_id= p_students,
                attendance_id = attendance,
            )
            attendance_report.save()
        messages.success(request, 'Your Attendance Submited Successful')

    return redirect('teacher_take_attendance')



def teacher_view_attendance(request):
    teacher_id = Teacher.objects.get(admin=request.user.id)
    course = Course.objects.filter(teacher_id = teacher_id)
    session_year = Session_Year.objects.all()

    action = request.GET.get('action')

    get_course=None
    get_session_year=None
    attendance_date=None
    attendance_report=None

    if action is not None:
        if request.method == "POST":
            course_id = request.POST.get('course_id')
            session_year_id = request.POST.get('session_id')
            attendance_date = request.POST.get('attendance_date')

            get_course = Course.objects.get(id=course_id)
            get_session_year = Session_Year.objects.get(id = session_year_id)
            attendance = Attendance.objects.filter(course_id=get_course, attendance_date=attendance_date)

            for i in attendance:
                attendance_id=i.id
                attendance_report=Attendance_Report.objects.filter(attendance_id=attendance_id)

    context = {
        'course' : course,
        'session_year':session_year,
        'action':action,
        'get_course':get_course,
        'get_session_year':get_session_year,
        'attendance_date':attendance_date,
        'attendance_report':attendance_report
    }
    return render(request, 'teacher/view_attendance.html', context)


