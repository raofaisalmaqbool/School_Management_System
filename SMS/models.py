from email.headerregistry import Address
from django.db import models

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
    Phone_No= models.CharField(max_length=11)

class Class(models.Model):
    ID = models.IntegerField(primary_key=True)
    