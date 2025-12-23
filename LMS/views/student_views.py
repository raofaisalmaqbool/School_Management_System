"""
Student-specific views for managing leave applications and viewing dashboard.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from LMS.models import Student, Student_Leave, Teacher, Course


@login_required(login_url='/')
def student_home(request):
    """
    Display student dashboard with statistics.
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
        return render(request, 'student/student_home.html', context)
    except Exception as e:
        messages.error(request, f'Error loading dashboard: {str(e)}')
        return render(request, 'student/student_home.html', {
            'teacher_count': 0,
            'student_count': 0,
            'course_count': 0
        })


# ==================== LEAVE APPLICATIONS ====================

@login_required(login_url='/')
def student_apply_leave(request):
    """
    Display student leave application form and history.
    Shows leave status: Pending (0), Approved (1), Rejected (2)
    """
    try:
        student = get_object_or_404(Student, admin=request.user.id)
        leave_history = Student_Leave.objects.filter(
            student_id=student
        ).order_by('-created_at')
        
        context = {'leave_history': leave_history}
        return render(request, 'student/student_leave_apply.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('student_home')
    except Exception as e:
        messages.error(request, f'Error loading leave history: {str(e)}')
        return render(request, 'student/student_leave_apply.html', {'leave_history': []})


@login_required(login_url='/')
def student_save_leave(request):
    """
    Save a new leave application for the student.
    """
    if request.method == "POST":
        try:
            leave_date = request.POST.get('leave_date')
            leave_message = request.POST.get('leave_message', '').strip()

            if not leave_date or not leave_message:
                messages.warning(request, 'Please provide both date and message.')
                return redirect('student_apply_leave')

            student = get_object_or_404(Student, admin=request.user.id)

            leave = Student_Leave(
                student_id=student,
                date=leave_date,
                message=leave_message,
            )
            leave.save()
            
            messages.success(request, 'Your leave application has been submitted successfully!')
        except Student.DoesNotExist:
            messages.error(request, 'Student profile not found.')
        except Exception as e:
            messages.error(request, f'Failed to submit leave application: {str(e)}')
    
    return redirect('student_apply_leave')
