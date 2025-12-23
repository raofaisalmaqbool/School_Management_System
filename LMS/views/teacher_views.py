"""
Teacher-specific views for managing attendance, notifications, and leave applications.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from LMS.models import (
    Course, Session_Year, Student, Attendance, Attendance_Report,
    Teacher, Teacher_Notification, Teacher_leave
)


@login_required(login_url='/')
def teacher_home(request):
    """
    Display teacher dashboard with statistics.
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
        return render(request, 'teacher/teacher_home.html', context)
    except Exception as e:
        messages.error(request, f'Error loading dashboard: {str(e)}')
        return render(request, 'teacher/teacher_home.html', {
            'teacher_count': 0,
            'student_count': 0,
            'course_count': 0
        })


# ==================== NOTIFICATIONS ====================

@login_required(login_url='/')
def notifications_teacher(request):
    """
    Display all notifications for the logged-in teacher.
    """
    try:
        teacher = get_object_or_404(Teacher, admin=request.user.id)
        notifications = Teacher_Notification.objects.filter(
            teacher_id=teacher
        ).order_by('-created_at')
        
        context = {'notifications': notifications}
        return render(request, 'teacher/teacher_notification.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher profile not found.')
        return redirect('teacher_home')
    except Exception as e:
        messages.error(request, f'Error loading notifications: {str(e)}')
        return render(request, 'teacher/teacher_notification.html', {'notifications': []})


@login_required(login_url='/')
def status_mark(request, status):
    """
    Mark a notification as read.
    """
    try:
        notification = get_object_or_404(Teacher_Notification, id=status)
        notification.status = 1
        notification.save()
        messages.success(request, 'Notification marked as read.')
    except Exception as e:
        messages.error(request, f'Failed to mark notification: {str(e)}')
    
    return redirect('notifications_teacher')


# ==================== LEAVE APPLICATIONS ====================

@login_required(login_url='/')
def teacher_leave_apply(request):
    """
    Display teacher leave application form and history.
    """
    try:
        teacher = get_object_or_404(Teacher, admin=request.user.id)
        leave_history = Teacher_leave.objects.filter(
            teacher_id=teacher
        ).order_by('-created_at')
        
        context = {'leave_history': leave_history}
        return render(request, 'teacher/teacher_leave_apply.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher profile not found.')
        return redirect('teacher_home')
    except Exception as e:
        messages.error(request, f'Error loading leave history: {str(e)}')
        return render(request, 'teacher/teacher_leave_apply.html', {'leave_history': []})


@login_required(login_url='/')
def teacher_leave_save(request):
    """
    Save a new leave application for the teacher.
    """
    if request.method == "POST":
        try:
            leave_date = request.POST.get('leave_date')
            leave_message = request.POST.get('leave_message', '').strip()

            if not leave_date or not leave_message:
                messages.warning(request, 'Please provide both date and message.')
                return redirect('teacher_leave_apply')

            teacher = get_object_or_404(Teacher, admin=request.user.id)

            leave = Teacher_leave(
                teacher_id=teacher,
                date=leave_date,
                message=leave_message,
            )
            leave.save()
            
            messages.success(request, 'Your leave application has been submitted successfully!')
        except Teacher.DoesNotExist:
            messages.error(request, 'Teacher profile not found.')
        except Exception as e:
            messages.error(request, f'Failed to submit leave application: {str(e)}')
    
    return redirect('teacher_leave_apply')


# ==================== ATTENDANCE MANAGEMENT ====================

@login_required(login_url='/')
def teacher_take_attendance(request):
    """
    Display form to take attendance for a course.
    """
    try:
        teacher = get_object_or_404(Teacher, admin=request.user.id)
        courses = Course.objects.filter(teacher=teacher)
        session_years = Session_Year.objects.all()

        action = request.GET.get('action')
        get_course = None
        students = None
        get_session_year = None

        if action is not None and request.method == "POST":
            course_id = request.POST.get('course_id')
            session_year_id = request.POST.get('session_id')

            if course_id and session_year_id:
                get_course = get_object_or_404(Course, id=course_id)
                get_session_year = get_object_or_404(Session_Year, id=session_year_id)

                # Get students enrolled in the selected course
                students = Student.objects.filter(course_id=course_id)

        context = {
            'courses': courses,
            'session_years': session_years,
            'get_course': get_course,
            'get_session_year': get_session_year,
            'action': action,
            'students': students,
        }
        return render(request, 'teacher/take_attendance.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher profile not found.')
        return redirect('teacher_home')
    except Exception as e:
        messages.error(request, f'Error loading attendance form: {str(e)}')
        return render(request, 'teacher/take_attendance.html', {
            'courses': [],
            'session_years': [],
            'students': None
        })


@login_required(login_url='/')
def teacher_save_attendance(request):
    """
    Save attendance records for students.
    """
    if request.method == "POST":
        try:
            course_id = request.POST.get('course_id')
            session_year_id = request.POST.get('session_id')
            attendance_date = request.POST.get('attendance_date')
            student_ids = request.POST.getlist('student_id')

            if not all([course_id, session_year_id, attendance_date]):
                messages.warning(request, 'Please provide all required information.')
                return redirect('teacher_take_attendance')

            get_course = get_object_or_404(Course, id=course_id)
            get_session_year = get_object_or_404(Session_Year, id=session_year_id)

            # Create attendance record
            attendance = Attendance(
                course_id=get_course,
                attendance_date=attendance_date,
                session_year_id=get_session_year,
            )
            attendance.save()

            # Save attendance for present students
            for student_id in student_ids:
                try:
                    student = get_object_or_404(Student, id=int(student_id))
                    attendance_report = Attendance_Report(
                        student_id=student,
                        attendance=attendance,
                    )
                    attendance_report.save()
                except (ValueError, Student.DoesNotExist):
                    continue

            messages.success(request, 'Attendance has been successfully recorded!')
        except Exception as e:
            messages.error(request, f'Failed to save attendance: {str(e)}')

    return redirect('teacher_take_attendance')


@login_required(login_url='/')
def teacher_view_attendance(request):
    """
    View attendance records for a specific course and date.
    """
    try:
        teacher = get_object_or_404(Teacher, admin=request.user.id)
        courses = Course.objects.filter(teacher=teacher)
        session_years = Session_Year.objects.all()

        action = request.GET.get('action')
        get_course = None
        get_session_year = None
        attendance_date = None
        attendance_reports = None

        if action is not None and request.method == "POST":
            course_id = request.POST.get('course_id')
            session_year_id = request.POST.get('session_id')
            attendance_date = request.POST.get('attendance_date')

            if all([course_id, session_year_id, attendance_date]):
                get_course = get_object_or_404(Course, id=course_id)
                get_session_year = get_object_or_404(Session_Year, id=session_year_id)
                
                # Get attendance record
                attendances = Attendance.objects.filter(
                    course_id=get_course,
                    attendance_date=attendance_date,
                    session_year_id=get_session_year
                )

                if attendances.exists():
                    attendance = attendances.first()
                    attendance_reports = Attendance_Report.objects.filter(
                        attendance=attendance
                    ).select_related('student_id__admin')

        context = {
            'courses': courses,
            'session_years': session_years,
            'action': action,
            'get_course': get_course,
            'get_session_year': get_session_year,
            'attendance_date': attendance_date,
            'attendance_reports': attendance_reports
        }
        return render(request, 'teacher/view_attendance.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher profile not found.')
        return redirect('teacher_home')
    except Exception as e:
        messages.error(request, f'Error loading attendance records: {str(e)}')
        return render(request, 'teacher/view_attendance.html', {
            'courses': [],
            'session_years': [],
            'attendance_reports': None
        })
