from distutils.command.upload import upload
from email.headerregistry import Address
import profile
from turtle import update
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


# Create your models here.
class Students(models.Model):
    ID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=50)
    Father_Name= models.CharField(max_length=50)
    Address=models.CharField(max_length=80)
    Phone_No= models.CharField(max_length=11)


class Teachers(models.Model):
    ID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=50)
    Address= models.CharField(max_length=50)
    Email=models.EmailField(max_length=54)
    Phone_No= models.CharField(max_length=80)

class Claass(models.Model):
    ID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=50)

class Customuser(AbstractUser):
    USER = (
        (1, 'PRINCIPAL'),
        (2, 'TEACHERS'),
        (3, 'STUDENTS'),
    )

    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')


class Course(models.Model):
    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): # this will return name either the course object 1,2,3
        return self.name
    
class Session_Year(models.Model):
    session_start = models.CharField(max_length=80)
    session_end = models.CharField(max_length=80)

    

    