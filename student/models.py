from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.core.exceptions import ValidationError
from django.urls import reverse

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(null=True,blank = True,unique=True,validators=[validators.EmailValidator,])
    

class Person(models.Model):
    fname = models.CharField(max_length=200,validators=[validators.MinLengthValidator(3)])
    lname = models.CharField(max_length=200,validators=[validators.MinLengthValidator(3)])
    address = models.CharField(max_length=200)
    


    class Meta:
        abstract = True

    def __str__(self):

         fullname = self.fname+' '+self.lname

         return fullname
        
    def fullname(self):
        return self.fname+' '+self.lname

    

class Supervisior(Person,models.Model):
    
    
    def get_absolute_url(self):

        return reverse('home')

class Subject(models.Model):
    name = models.CharField(max_length=200, validators=[validators.MinLengthValidator(3),],unique=True)
    teacher = models.ManyToManyField(Supervisior,related_name='enrolled')
    

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):

        return reverse('home')


class Faculty(models.Model):

    name = models.CharField(max_length=200,validators=[validators.MinLengthValidator(3)],unique=True)
    teacher = models.ManyToManyField(Supervisior,related_name='supervisor')
    subject = models.ManyToManyField(Subject,related_name="contains")

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):

        return reverse('home')



class Student(Person, models.Model):

     photo = models.ImageField(upload_to ='static/uploads/')
     email = models.EmailField(validators=[validators.EmailValidator,],unique=True)
     DOB = models.DateField()
     age = models.IntegerField(validators=[validators.MinValueValidator(1),validators.MinValueValidator(25)],null=True)
     grade = models.IntegerField(validators=[validators.MinValueValidator(10),validators.MinValueValidator(12)])
     roll_no = models.IntegerField(validators=[validators.MinValueValidator(1)],unique=True)
     faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE,related_name='enrolled')
     
     
     

     def get_absolute_url(self):

        return reverse('student_details', args=[str(self.id)])