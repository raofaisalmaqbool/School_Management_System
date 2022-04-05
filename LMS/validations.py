import email
from this import d
from django.db import models
import re

# # class Form_Validation():
# class Form_Validation():
from LMS.models import Course, Customuser, Session_Year, Student, Student_Leave, Teacher, Teacher_Notification, Teacher_leave

from django.contrib import messages
from django.shortcuts import render, redirect
from urllib import request
from LMS.models import Customuser


d = {}
class Validation:
    # def __init__(self):
    #     add_teacher


    @staticmethod
    def f_name(self, xname=None):
        if xname == None:
            d['e1'] = "please enter first name"
            return d
        elif not xname.isalpha():
            d['e1'] = "please enter correct first name"
            return d

    
    @staticmethod
    def l_name(self, yname=None):
        if yname == None:
            d['e1'] = "please enter last name"
            return d
        elif not yname.isalpha():
            d['e1'] = "please enter correct last name"
            return d
            


# valid_a = Validation()

    

