"""School_Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path
from SMS import views
from django.conf import settings
from django.conf.urls.static import static
from.import principal_views, teachers_views, students_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='home'),
    path('base/', views.base, name='base'),
    path('', views.login, name='login'),
    path('doLogin/', views.doLogin, name='doLogin'),
    path('doLogout/', views.doLogout, name='logout'),
    path('profile/', views.profile, name="profile"),
    path('principal/principal_home/', principal_views.principal_home, name='principal_home'),  #principal home page
    path('profile/update', views.profile_update, name='profile_update'),
    #path('Profile/update',views.PROFILE_UPDATE,name='profile_update'),
    #path('Hod/Student/Add',Hod_Views.ADD_STUDENT,name='add_student'),
    path('principal/student/add',principal_views.add_student, name='add_student'),
    path('principal/student/view',principal_views.view_student,name='view_student'),
    path('principal/student/edit/<str:id>',principal_views.edit_student,name='edit_student'),
    path('principal/student/update',principal_views.update_student,name='update_student'),
    path('principal/student/delete/<str:admin>',principal_views.delete_student,name='delete_student'),
    path('principal/course/add',principal_views.add_course,name='add_course'),




] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
