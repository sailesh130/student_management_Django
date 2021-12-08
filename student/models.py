from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.
Capital_validator = RegexValidator('^[A-Z][a-z]*$','Should start with uppercase')

class UserManager(BaseUserManager):
    def create_user(self,username, email ,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, email, password):
        user = self.create_user(
            username = username,
            email = email,
            password=password,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    email = models.EmailField(null=True,blank = True,unique=True,validators=[validators.EmailValidator,])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Person(models.Model):
    fname = models.CharField(max_length=200,validators=[validators.MinLengthValidator(3),Capital_validator])
    lname = models.CharField(max_length=200,validators=[validators.MinLengthValidator(3),Capital_validator])
    address = models.CharField(max_length=200)
    


    class Meta:
        abstract = True

    def __str__(self):

         fullname = self.fname+' '+self.lname

         return fullname

        
    def fullname(self):
        return self.fname+' '+self.lname

    

class Supervisior(Person,models.Model):
    pass
    
    

class Subject(models.Model):
    name = models.CharField(max_length=200, validators=[validators.MinLengthValidator(3),Capital_validator],unique=True)
    teacher = models.ManyToManyField(Supervisior,related_name='enrolled')
    

    def __str__(self):
        return f"{self.name}"



class Faculty(models.Model):

    name = models.CharField(max_length=200,validators=[validators.MinLengthValidator(3),Capital_validator],unique=True)
    teacher = models.ManyToManyField(Supervisior,related_name='supervisor')
    subject = models.ManyToManyField(Subject,related_name="contains")

    def __str__(self):
        return f"{self.name}"




class Student(Person, models.Model):

     photo = models.ImageField(upload_to ='static/uploads/')
     email = models.EmailField(validators=[validators.EmailValidator,],unique=True)
     DOB = models.DateField()
     age = models.IntegerField(validators=[validators.MinValueValidator(1),validators.MinValueValidator(25)],null=True)
     grade = models.IntegerField(validators=[validators.MinValueValidator(10),validators.MinValueValidator(12)])
     roll_no = models.IntegerField(validators=[validators.MinValueValidator(1)],unique=True)
     faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE,related_name='enrolled')
     
     
     
