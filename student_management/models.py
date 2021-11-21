from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Faculty(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

class Supervisior(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

class Subject(models.Model):
    name = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE,related_name='contains')

    def __str__(self):
        return f"{self.name}"

class Student(models.Model):
     name = models.CharField(max_length=200)
     age = models.IntegerField()
     grade = models.IntegerField()
     address = models.CharField(max_length=200)
     roll_no = models.IntegerField()
     supervisior = models.ForeignKey(Supervisior,on_delete=models.CASCADE,related_name='supervise')
     faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE,related_name='enrolled')
     subject = models.ManyToManyField(Subject,related_name="contains")

     def __str__(self):
        return f"{self.name}"





