from django.db import models


# class Form_Validation():
from django.contrib import messages
from django.shortcuts import render, redirect
from urllib import request


def validations(profile_pic, first_name):
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
    if not first_name.isalpha() or first_name != "":
        # messages.warning(request, 'please correct enter first name')
        # return redirect('add_student')
        # num = num+1
        d['e2'] = "please enter correct first name"
        # d['num'] = d['num'] + 1

    return d