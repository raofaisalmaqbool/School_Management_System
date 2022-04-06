from django.shortcuts import render, redirect, HttpResponse
from LMS.emailbackend import EmailBackend
from django.contrib.auth import authenticate, login as logino, logout
from django.contrib import messages
from LMS.models import Customuser
from django.contrib.auth.decorators import login_required
from .forms import CustomForm
# Create your views here.
def index(request):
    return render(request,'index.html')

def base(request):
    return render(request, 'base.html')

def login(request):
    print("in login function views.py")
    return render(request, 'login.html')

def doLogout(request):
    print("in dologout function views.py")
    logout(request)
    return render(request, 'login.html')

def doLogin(request):
    print("in dologin function views.py")
    if request.method == "POST":
       user = EmailBackend.authenticate(request,
                                        username=request.POST.get('email'),
                                        password=request.POST.get('password'),)
       if user!=None:
           print("in dologin function views.py",user.user_type)
           logino(request,user)
           user_type = user.user_type
           if user_type == '1':
               return redirect('principal_home')
           elif user_type == '2':
               return redirect('teacher_home')
           elif user_type == '3':
               return redirect('student_home')
           else:
               messages.error(request,'Email or Password are Invalid !')
               return redirect('login')
       else:
           messages.error(request,'Email or Password are Invalid !')
           return redirect('login')

@login_required(login_url='/')
def profile(request):
    user = Customuser.objects.get(id = request.user.id)


    context = {
        "user":user,
    }
    return render(request,'profile.html',context)

@login_required(login_url='/')
def profile_update(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        #email = request.POST.get('email')
        #username = request.POST.get('username')
        password = request.POST.get('password')
        print(profile_pic)
        try:
            customuser = Customuser.objects.get(id = request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name

            if password !=None and password != "":
                customuser.set_password(password)
            if profile_pic !=None and profile_pic != "":
                customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,'Your Profile Updated Successfully !')
            return redirect('profile')
        except:
            messages.error(request,'Failed To Update Your Profile')

    return render(request,'profile.html')



def test_form(request):
    
    if request.method == "POST":
        Cfor = CustomForm(request.POST)
        print(Cfor)
        print("post request")
        if Cfor.is_valid:
            print("if data validate")
            name = Cfor.cleaned_data['name']      # not valid mathod for get data, ya cleanded data ni dy ga
            email = Cfor.cleaned_data['email']   # valid method , cleand data dy ga
            password = Cfor.cleaned_data['password']
            print('name :', name)
            print('email :', email)
            print('password :', password)
            
        
    else:
        Cfor = CustomForm()
        print("get request")
    return render(request, 'test_form.html', {'testform':Cfor})
