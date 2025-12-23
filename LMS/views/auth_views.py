"""
Authentication and user profile views for the LMS application.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from LMS.emailbackend import EmailBackend
from LMS.models import Customuser


def index(request):
    """Display the home/index page."""
    return render(request, 'index.html')


def base(request):
    """Display the base template (for testing purposes)."""
    return render(request, 'base.html')


def login(request):
    """Display the login page."""
    return render(request, 'login.html')


def doLogout(request):
    """
    Log out the current user and redirect to login page.
    """
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')


def doLogin(request):
    """
    Authenticate user and redirect to appropriate dashboard based on user type.
    
    User Types:
        - '1': Principal -> principal_home
        - '2': Teacher -> teacher_home
        - '3': Student -> student_home
    """
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validate input
        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return redirect('login')
        
        # Authenticate user
        user = EmailBackend.authenticate(
            EmailBackend(),
            request=request,
            username=email,
            password=password
        )
        
        if user is not None:
            auth_login(request, user)
            user_type = user.user_type
            
            # Redirect based on user type
            if user_type == '1':
                messages.success(request, f'Welcome back, Principal {user.first_name}!')
                return redirect('principal_home')
            elif user_type == '2':
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('teacher_home')
            elif user_type == '3':
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('student_home')
            else:
                messages.error(request, 'Invalid user type.')
                logout(request)
                return redirect('login')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    
    return redirect('login')


@login_required(login_url='/')
def profile(request):
    """
    Display user profile page.
    """
    try:
        user = Customuser.objects.get(id=request.user.id)
        context = {'user': user}
        return render(request, 'profile.html', context)
    except Customuser.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('home')


@login_required(login_url='/')
def profile_update(request):
    """
    Update user profile information including name, password, and profile picture.
    """
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '').strip()
        
        try:
            customuser = Customuser.objects.get(id=request.user.id)
            
            # Update basic information
            if first_name:
                customuser.first_name = first_name
            if last_name:
                customuser.last_name = last_name
            
            # Update password if provided
            if password:
                customuser.set_password(password)
            
            # Update profile picture if provided
            if profile_pic:
                customuser.profile_pic = profile_pic
            
            customuser.save()
            
            # Re-authenticate user if password was changed
            if password:
                auth_login(request, customuser)
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
            
        except Customuser.DoesNotExist:
            messages.error(request, 'User not found.')
        except Exception as e:
            messages.error(request, f'Failed to update profile: {str(e)}')
    
    return render(request, 'profile.html')
