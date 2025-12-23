"""
Principal-specific views for managing students, teachers, courses, and leaves.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from LMS.models import (
    Course, Customuser, Session_Year, Student, Student_Leave,
    Teacher, Teacher_Notification, Teacher_leave
)


@login_required(login_url='/')
def principal_home(request):
    """
    Display principal dashboard with statistics.
    """
    try:
        teacher_count = Teacher.objects.count()
        student_count = Student.objects.count()
        course_count = Course.objects.count()

        context = {
            'teacher_count': teacher_count,
            'student_count': student_count,
            'course_count': course_count
        }
        return render(request, 'principal/principal_home.html', context)
    except Exception as e:
        messages.error(request, f'Error loading dashboard: {str(e)}')
        return render(request, 'principal/principal_home.html', {'teacher_count': 0, 'student_count': 0, 'course_count': 0})


# ==================== STUDENT MANAGEMENT ====================

@login_required(login_url='/')
def add_student(request):
    """
    Add a new student to the system.
    """
    courses = Course.objects.all()
    session_years = Session_Year.objects.all()

    if request.method == "POST":
        try:
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            address = request.POST.get('address', '').strip()
            gender = request.POST.get('gender', '').strip()
            course_id = request.POST.get('course_id')
            session_year_id = request.POST.get('session_year_id')

            # Validation
            if not all([first_name, last_name, email, username, password, address, gender, course_id, session_year_id]):
                messages.warning(request, 'Please fill in all required fields.')
                return redirect('add_student')

            if Customuser.objects.filter(email=email).exists():
                messages.warning(request, 'Email is already taken.')
                return redirect('add_student')

            if Customuser.objects.filter(username=username).exists():
                messages.warning(request, 'Username is already taken.')
                return redirect('add_student')

            # Create user
            user = Customuser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type='3'
            )
            user.set_password(password)
            user.save()

            # Create student
            course = Course.objects.get(id=course_id)
            session_year = Session_Year.objects.get(id=session_year_id)

            student = Student(
                admin=user,
                address=address,
                session_year_id=session_year,
                course_id=course,
                gender=gender,
            )
            student.save()
            
            messages.success(request, f'{user.first_name} {user.last_name} has been successfully added as a student!')
            return redirect('add_student')

        except Course.DoesNotExist:
            messages.error(request, 'Selected course does not exist.')
        except Session_Year.DoesNotExist:
            messages.error(request, 'Selected session year does not exist.')
        except Exception as e:
            messages.error(request, f'Failed to add student: {str(e)}')

    context = {
        'courses': courses,
        'session_years': session_years,
    }
    return render(request, 'principal/add_student.html', context)


@login_required(login_url='/')
def view_student(request):
    """
    Display list of all students.
    """
    try:
        students = Student.objects.select_related('admin', 'course_id', 'session_year_id').all()
        context = {'students': students}
        return render(request, 'principal/view_student.html', context)
    except Exception as e:
        messages.error(request, f'Error loading students: {str(e)}')
        return render(request, 'principal/view_student.html', {'students': []})


@login_required(login_url='/')
def edit_student(request, id):
    """
    Display form to edit student details.
    """
    try:
        student = get_object_or_404(Student, id=id)
        courses = Course.objects.all()
        session_years = Session_Year.objects.all()

        context = {
            'student': student,
            'courses': courses,
            'session_years': session_years,
        }
        return render(request, 'principal/edit_student.html', context)
    except Exception as e:
        messages.error(request, f'Error loading student: {str(e)}')
        return redirect('view_student')


@login_required(login_url='/')
def update_student(request):
    """
    Update student information.
    """
    if request.method == "POST":
        try:
            student_id = request.POST.get('student_id')
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            address = request.POST.get('address', '').strip()
            gender = request.POST.get('gender', '').strip()
            course_id = request.POST.get('course_id')
            session_year_id = request.POST.get('session_year_id')

            # Update user
            user = get_object_or_404(Customuser, id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username

            if password:
                user.set_password(password)
            if profile_pic:
                user.profile_pic = profile_pic
            user.save()

            # Update student
            student = get_object_or_404(Student, admin=student_id)
            student.address = address
            student.gender = gender

            course = get_object_or_404(Course, id=course_id)
            student.course_id = course

            session_year = get_object_or_404(Session_Year, id=session_year_id)
            student.session_year_id = session_year

            student.save()
            
            messages.success(request, 'Student record has been successfully updated!')
            return redirect('view_student')

        except Exception as e:
            messages.error(request, f'Failed to update student: {str(e)}')

    return redirect('view_student')


@login_required(login_url='/')
def delete_student(request, admin):
    """
    Delete a student from the system.
    """
    try:
        user = get_object_or_404(Customuser, id=admin)
        user.delete()
        messages.success(request, 'Student has been successfully deleted!')
    except Exception as e:
        messages.error(request, f'Failed to delete student: {str(e)}')
    
    return redirect('view_student')


# ==================== COURSE MANAGEMENT ====================

@login_required(login_url='/')
def add_course(request):
    """
    Add a new course to the system.
    """
    if request.method == "POST":
        try:
            course_name = request.POST.get('course_name', '').strip()

            if not course_name:
                messages.warning(request, 'Please enter a course name.')
                return redirect('add_course')

            if Course.objects.filter(name=course_name).exists():
                messages.warning(request, 'Course already exists.')
                return redirect('add_course')

            course = Course(name=course_name)
            course.save()
            
            messages.success(request, 'Course has been successfully created!')
            return redirect('add_course')

        except Exception as e:
            messages.error(request, f'Failed to add course: {str(e)}')

    return render(request, 'principal/add_course.html')


@login_required(login_url='/')
def view_course(request):
    """
    Display list of all courses.
    """
    try:
        courses = Course.objects.all()
        context = {'courses': courses}
        return render(request, 'principal/view_course.html', context)
    except Exception as e:
        messages.error(request, f'Error loading courses: {str(e)}')
        return render(request, 'principal/view_course.html', {'courses': []})


@login_required(login_url='/')
def edit_course(request, id):
    """
    Display form to edit course details.
    """
    try:
        course = get_object_or_404(Course, id=id)
        context = {'course': course}
        return render(request, 'principal/edit_course.html', context)
    except Exception as e:
        messages.error(request, f'Error loading course: {str(e)}')
        return redirect('view_course')


@login_required(login_url='/')
def update_course(request):
    """
    Update course information.
    """
    if request.method == "POST":
        try:
            name = request.POST.get('name', '').strip()
            course_id = request.POST.get('course_id')

            if not name:
                messages.warning(request, 'Please enter a course name.')
                return redirect('view_course')

            course = get_object_or_404(Course, id=course_id)
            course.name = name
            course.save()
            
            messages.success(request, 'Course has been successfully updated!')
            return redirect('view_course')

        except Exception as e:
            messages.error(request, f'Failed to update course: {str(e)}')

    return redirect('view_course')


@login_required(login_url='/')
def delete_course(request, id):
    """
    Delete a course from the system.
    """
    try:
        course = get_object_or_404(Course, id=id)
        course.delete()
        messages.success(request, 'Course has been successfully deleted!')
    except Exception as e:
        messages.error(request, f'Failed to delete course: {str(e)}')
    
    return redirect('view_course')


# ==================== TEACHER MANAGEMENT ====================

@login_required(login_url='/')
def add_teacher(request):
    """
    Add a new teacher to the system.
    """
    if request.method == "POST":
        try:
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            address = request.POST.get('address', '').strip()
            gender = request.POST.get('gender', '').strip()

            # Validation
            if not all([first_name, last_name, email, username, password, address, gender]):
                messages.warning(request, 'Please fill in all required fields.')
                return redirect('add_teacher')

            if Customuser.objects.filter(email=email).exists():
                messages.warning(request, 'Email is already taken.')
                return redirect('add_teacher')

            if Customuser.objects.filter(username=username).exists():
                messages.warning(request, 'Username is already taken.')
                return redirect('add_teacher')

            # Create user
            user = Customuser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type='2'
            )
            user.set_password(password)
            user.save()

            # Create teacher
            teacher = Teacher(
                admin=user,
                address=address,
                gender=gender,
            )
            teacher.save()
            
            messages.success(request, f'{user.first_name} {user.last_name} has been successfully added as a teacher!')
            return redirect('add_teacher')

        except Exception as e:
            messages.error(request, f'Failed to add teacher: {str(e)}')

    return render(request, 'principal/add_teacher.html')


@login_required(login_url='/')
def view_teacher(request):
    """
    Display list of all teachers.
    """
    try:
        teachers = Teacher.objects.select_related('admin').all()
        context = {'teachers': teachers}
        return render(request, 'principal/view_teacher.html', context)
    except Exception as e:
        messages.error(request, f'Error loading teachers: {str(e)}')
        return render(request, 'principal/view_teacher.html', {'teachers': []})


@login_required(login_url='/')
def edit_teacher(request, id):
    """
    Display form to edit teacher details.
    """
    try:
        teacher = get_object_or_404(Teacher, id=id)
        context = {'teacher': teacher}
        return render(request, 'principal/edit_teacher.html', context)
    except Exception as e:
        messages.error(request, f'Error loading teacher: {str(e)}')
        return redirect('view_teacher')


@login_required(login_url='/')
def delete_teacher(request, admin):
    """
    Delete a teacher from the system.
    """
    try:
        user = get_object_or_404(Customuser, id=admin)
        user.delete()
        messages.success(request, 'Teacher has been successfully deleted!')
    except Exception as e:
        messages.error(request, f'Failed to delete teacher: {str(e)}')
    
    return redirect('view_teacher')


# ==================== TEACHER NOTIFICATIONS ====================

@login_required(login_url='/')
def teacher_send_notification(request):
    """
    Display form to send notifications to teachers.
    """
    try:
        teachers = Teacher.objects.select_related('admin').all()
        notifications = Teacher_Notification.objects.select_related('teacher_id__admin').order_by('-created_at')
        
        context = {
            'teachers': teachers,
            'notifications': notifications,
        }
        return render(request, 'principal/teacher_notification.html', context)
    except Exception as e:
        messages.error(request, f'Error loading notifications: {str(e)}')
        return render(request, 'principal/teacher_notification.html', {'teachers': [], 'notifications': []})


@login_required(login_url='/')
def save_teacher_notification(request):
    """
    Save a new notification for a teacher.
    """
    if request.method == "POST":
        try:
            teacher_id = request.POST.get('teacher_id')
            message = request.POST.get('message', '').strip()

            if not message:
                messages.warning(request, 'Please enter a message.')
                return redirect('teacher_send_notification')

            teacher = get_object_or_404(Teacher, admin=teacher_id)
            notification = Teacher_Notification(
                teacher_id=teacher,
                message=message,
            )
            notification.save()
            
            messages.success(request, 'Notification has been successfully sent!')
        except Exception as e:
            messages.error(request, f'Failed to send notification: {str(e)}')
    
    return redirect('teacher_send_notification')


# ==================== LEAVE MANAGEMENT ====================

@login_required(login_url='/')
def teacher_leave_view(request):
    """
    Display all teacher leave applications.
    """
    try:
        teacher_leaves = Teacher_leave.objects.select_related('teacher_id__admin').order_by('-created_at')
        context = {'teacher_leaves': teacher_leaves}
        return render(request, 'principal/teacher_leave.html', context)
    except Exception as e:
        messages.error(request, f'Error loading teacher leaves: {str(e)}')
        return render(request, 'principal/teacher_leave.html', {'teacher_leaves': []})


@login_required(login_url='/')
def teacher_leave_approve(request, id):
    """
    Approve a teacher leave application.
    """
    try:
        leave = get_object_or_404(Teacher_leave, id=id)
        leave.status = 1
        leave.save()
        messages.success(request, 'Leave application has been approved!')
    except Exception as e:
        messages.error(request, f'Failed to approve leave: {str(e)}')
    
    return redirect('teacher_leave_view')


@login_required(login_url='/')
def teacher_leave_disapprove(request, id):
    """
    Reject a teacher leave application.
    """
    try:
        leave = get_object_or_404(Teacher_leave, id=id)
        leave.status = 2
        leave.save()
        messages.success(request, 'Leave application has been rejected!')
    except Exception as e:
        messages.error(request, f'Failed to reject leave: {str(e)}')
    
    return redirect('teacher_leave_view')


@login_required(login_url='/')
def student_leave_view(request):
    """
    Display all student leave applications.
    """
    try:
        student_leaves = Student_Leave.objects.select_related('student_id__admin').order_by('-created_at')
        context = {'student_leaves': student_leaves}
        return render(request, 'principal/student_leave.html', context)
    except Exception as e:
        messages.error(request, f'Error loading student leaves: {str(e)}')
        return render(request, 'principal/student_leave.html', {'student_leaves': []})


@login_required(login_url='/')
def student_leave_approve(request, id):
    """
    Approve a student leave application.
    """
    try:
        leave = get_object_or_404(Student_Leave, id=id)
        leave.status = 1
        leave.save()
        messages.success(request, 'Leave application has been approved!')
    except Exception as e:
        messages.error(request, f'Failed to approve leave: {str(e)}')
    
    return redirect('student_leave_view')


@login_required(login_url='/')
def student_leave_disapprove(request, id):
    """
    Reject a student leave application.
    """
    try:
        leave = get_object_or_404(Student_Leave, id=id)
        leave.status = 2
        leave.save()
        messages.success(request, 'Leave application has been rejected!')
    except Exception as e:
        messages.error(request, f'Failed to reject leave: {str(e)}')
    
    return redirect('student_leave_view')
