from email import message
from http.client import HTTPResponse
from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from SMS.models import Course, Customuser, Session_Year, Student, Student_Leave, Teacher, Teacher_Notification,Teacher_leave
from django.contrib import messages
from SMS.models import Student
  
@login_required(login_url='/')
def principal_home(request):
    teacher_count = Teacher.objects.all().count() # they will return total no of teachre, studnt ,courses
    student_count = Student.objects.all().count()
    course_count = Course.objects.all().count()

    context ={
        'teacher_count' : teacher_count,
        'student_count' : student_count,
        'course_count' : course_count
    }

    return render(request, 'principal/principal_home.html', context)

@login_required(login_url='/')
def add_student(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        if Customuser.objects.filter(email=email).exists():
           messages.warning(request,'Email Is Already Taken')
           return redirect('add_student')
        if Customuser.objects.filter(username=username).exists():
           messages.warning(request,'Username Is Already Taken')
           return redirect('add_student')
        else:
            user = Customuser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 3
            )
            user.set_password(password)
            user.save()

            course = Course.objects.get(id=course_id)
            session_year = Session_Year.objects.get(id=session_year_id)

            student = Student(
                admin = user,
                address = address,
                session_year_id = session_year,
                course_id = course,
                gender = gender,
            )
            student.save()
            messages.success(request, user.first_name + "  " + user.last_name + " student are Successfully Added !")
            return redirect('add_student')

    context = {
        'course':course,
        'session_year':session_year,
    }
    return render(request,'principal/add_student.html', context)

@login_required(login_url='/')
def view_student(request):
    return render(request,'principal/view_student.html')

@login_required(login_url='/')
def view_student(request):
    student = Student.objects.all()

    context = {
        'student':student,
    }
    return render(request,'principal/view_student.html',context)

@login_required(login_url='/')
def edit_student(request,id):
    student = Student.objects.filter(id = id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    context = {
        'student':student,
        'course':course,
        'session_year':session_year,
    }
    return render(request,'principal/edit_student.html',context)


@login_required(login_url='/')
def update_student(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        print(student_id)
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        user = Customuser.objects.get(id = student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin = student_id)
        student.address = address
        student.gender = gender

        course = Course.objects.get(id = course_id)
        student.course_id = course

        session_year = Session_Year.objects.get(id = session_year_id)
        student.session_year_id = session_year

        student.save()
        messages.success(request,'Student Record Are Successfully Updated !')
        return redirect('view_student')

    return render(request,'principal/edit_student.html')
#34 update student (Backend).txt
 #34 update student (Backend).txt.

@login_required(login_url='/')
def delete_student(request,admin):
    student = Customuser.objects.get(id = admin)
    student.delete()
    messages.success(request,'Record Are Successfully Deleted !')
    return redirect('view_student')


@login_required(login_url='/')
def add_course(request):

    if request.method == "POST":
        course_name = request.POST.get('course_name')

        course = Course(
            name = course_name,
        )
        course.save()
        messages.success(request,'Course Are Successfully Created ')

        
        return redirect('add_course')

    return render(request,'principal/add_course.html')


@login_required(login_url='/')
def view_course(request):
    course = Course.objects.all()
    context = {
        'course':course,
    }
    return render(request,'principal/view_course.html',context)

@login_required(login_url='/')
def edit_course(request, id):
    course = Course.objects.get(id=id)
    context = {
        'course' : course
    }
    return render(request, 'principal/edit_course.html', context)

def update_course(request):
    if request.method == "POST":
        name = request.POST.get('name')# form ky ander course name ko bhaja tha name ky title sy osko yahan per get kiya ha
        course_id = request.POST.get('course_id')# or course id bhaji thi edit_course ma wo get krwai

        course = Course.objects.get(id = course_id) #models ma say course object ki id mil jay gi issy
        course.name = name  # for course name change
        course.save()
        messages.success(request, 'Course Updated Successfully!')
        return redirect('view_course')

    return render(request, 'principal/edit_course.html')

def delete_course(request, id):
    course = Course.objects.get(id=id)    # ya model ki id laye ga
    course.delete()        # will delete the course
    messages.success(request,'Course is deleted!')
    return redirect('view_course')


def add_teacher(request):
    if request.method == "POST":     # it will get the post request
        profile_pic = request.FILES.get('profile_pic')  # this will get the data from fom and save it
        first_name = request.POST.get('first_name')     # in the variable 
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if Customuser.objects.filter(email=email).exists():
           messages.warning(request,'Email Is Already Taken')
           return redirect('add_teacher')
        if Customuser.objects.filter(username=username).exists():
           messages.warning(request,'Username Is Already Taken')
           return redirect('add_teacher')
        
        else:
            user = Customuser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 2
            )
            user.set_password(password)     # password is equal to password nahi likh sakty is liya 
            user.save()

            teacher = Teacher(
                admin = user,
                address = address,
                gender = gender,
            )
            teacher.save()
            messages.success(request, user.first_name + "  " + user.last_name + " Teacher is Successfully Added !")
            return redirect('add_teacher')

    return render(request, "principal/add_teacher.html")

def view_teacher(request):
    teacher = Teacher.objects.all()
    context ={
        'teacher' : teacher
    }
    return render(request, 'principal/view_teacher.html', context)


def edit_teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    context ={
        'teacher':teacher
    }
    return render(request, "principal/edit_teacher.html", context)

def delete_teacher(request, admin):
    teacher = Customuser.objects.get(id = admin)
    teacher.delete()
    messages.success(request, 'Record Successfully!')
    #return render(request, 'principal/view_teacher.html')
    return redirect('view_teacher')



def teacher_send_notifiction(request):
    teacher = Teacher.objects.all()
    see_notification = Teacher_Notification.objects.all().order_by('-id')
    context ={
        'teacher' : teacher,
        'see_notification' : see_notification,
    }
    return render(request, 'principal/teacher_notification.html', context)


def save_teacher_notification(request):
    if request.method == "POST":
        teacher_id = request.POST.get('teacher_id')
        message = request.POST.get('message')

        #print(teacher_id, message)

        teacher = Teacher.objects.get(admin = teacher_id)
        notifcation = Teacher_Notification(
            teacher_id = teacher,
            message = message,

        )
        notifcation.save()
        messages.success(request, 'Your Notification Success Send')
    return redirect('teacher_send_notifiction')


def teacher_leave_view(request): 
    teacher_leave = Teacher_leave.objects.all()
    context ={
        'teacher_leave' : teacher_leave
    }
    return render(request, 'principal/teacher_leave.html', context)



def teacher_leave_approve(request, id):
    leave = Teacher_leave.objects.get(id = id)
    leave.status = 1
    leave.save()
    return redirect('teacher_leave_view')
    

def teacher_leave_disapprove(requesst, id):
    leave = Teacher_leave.objects.get(id = id)
    leave.status = 2
    leave.save()
    return redirect('teacher_leave_view')


def student_leave_view(request):
    student_leave = Student_Leave.objects.all()
    context = {
        'student_leave' : student_leave
    }
    return render(request, 'principal/student_leave.html', context)


def student_leave_approve(request, id):
    leave = Student_Leave.objects.get(id = id)
    leave.status = 1
    leave.save()
    return redirect('student_leave_view')
    

def student_leave_disapprove(requesst, id):
    leave = Student_Leave.objects.get(id = id)
    leave.status = 2
    leave.save()
    return redirect('student_leave_view')