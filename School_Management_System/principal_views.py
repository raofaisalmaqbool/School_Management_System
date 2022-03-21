from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from SMS.models import Course, Customuser, Session_Year, Student 
from django.contrib import messages

@login_required(login_url='/')
def principal_home(request):
    return render(request, 'principal/principal_home.html')

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