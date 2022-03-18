from django.shortcuts import render, redirect, HttpResponse
from SMS.emailbackend import EmailBackend
from django.contrib.auth import authenticate, login as logino, logout
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'index.html')

def base(request):
    return render(request, 'base.html')

def login(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method == "POST":
       user = EmailBackend.authenticate(request,
                                        username=request.POST.get('email'),
                                        password=request.POST.get('password'),)
       if user!=None:
           logino(request,user)
           user_type = user.user_type
           if user_type == '1':
               return HttpResponse('This is Hod Panel')
           elif user_type == '2':
               return HttpResponse('This is Staff Panel')
           elif user_type == '3':
               return HttpResponse('This is Student Panel')
           else:
               messages.error(request,'Email or Password are Invalid !')
               return redirect('login')
       else:
           messages.error(request,'Email or Password are Invalid !')
           return redirect('login')