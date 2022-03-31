
import email
from django.db import models
import re


# class Form_Validation():
from SMS.models import Course, Customuser, Session_Year, Student, Student_Leave, Teacher, Teacher_Notification, Teacher_leave

from django.contrib import messages
from django.shortcuts import render, redirect
from urllib import request

from SMS.models import Customuser


def validations(profile_pic, first_name, last_name, email, username):
    d = {}
    # validation for empty first_name
    # num = 0
    if not first_name:
        # messages.warning(request, 'please enter first name')
        # return redirect('add_student')
        d['e1'] = "please enter first name"
        # d['num'] = d['num'] + 1
        # num = num+1

    # validation for correct enter first_name
    if not first_name.isalpha() and first_name != "":
        # messages.warning(request, 'please correct enter first name')
        # return redirect('add_student')
        # num = num+1
        d['e2'] = "please enter correct first name"
        # d['num'] = d['num'] + 1

    # validation for empty last_name
    if not last_name:
        # messages.warning(request, 'please enter first name')
        # return redirect('add_student')
        d['e3'] = "please enter last name"
        # d['num'] = d['num'] + 1
        # num = num+1

    # validation for correct enter last_name
    if not last_name.isalpha() and last_name != "":
        # messages.warning(request, 'please correct enter first name')
        # return redirect('add_student')
        # num = num+1
        d['e4'] = "please enter correct last name"
        # d['num'] = d['num'] + 1

    regex = '''!#$%&'() *+,-"/:;<=>?[\]^_`{|}~'''
    abc = str(email)
    for i in abc:
        if i in regex:
            d['e5'] = "invalid email"

    if not username.isalnum() or username == "":
        d['e6'] = "something wrong with username please use alphabet or numeric numbers"

    pic_name = str(profile_pic)
    exa = ".png"
    exb = ".jpg"

    # ab =""
    # print(pic_name)
    # for i in pic_name[-4::1]:
    #     ab = ab.append(i)
    if exa in pic_name or exb in pic_name or pic_name=="None": #profile_pic == None
        # print(pic_name)
        pass
    else:
        d['e7'] = "invalid image not PNG or JPG"



    if Customuser.objects.filter(username=username).exists():
        d['e8'] = "username Is Already Taken"

    if Customuser.objects.filter(email=email).exists():
        d['e9'] = "Email Is Already Taken"


    # if Customuser.objects.filter(email=email).exists():
    #     d['e6'] = "Email Is Already Taken"
        # messages.warning(request, 'Email Is Already Taken')

    # email1 = email.split("@")[0]
    # email2 = email.split("@")[-1]
    # if not email1.isalnum():
    #     d['e5'] = "only google gmail is allowed"

    return d
