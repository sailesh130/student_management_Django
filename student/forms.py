from typing import DefaultDict
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.views.generic.list import ListView
from .models import CustomUser, Faculty, Student, Subject, Supervisior
from django.forms import ModelForm, fields
from django.core.exceptions import ValidationError
import datetime


class CustomUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 !=password2:
            raise forms.ValidationError("Password does not match")
        return password2


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class StudentForm(ModelForm):
    
    field_order = ['fname','lname', 'address', 'DOB','email','grade','roll_no','photo','faculty']
    class Meta:
        model = Student
        exclude = ('age',)
        widgets = {"DOB":forms.DateInput(attrs={'type': 'date'})}


    def name(self,student):
        f_name = self.cleaned_data.get('fname')
        l_name = self.cleaned_data.get('lname')
        student.fname = f_name.capitalize()
        student.lname = l_name.capitalize()

    def dob(self,student):
        DOB = self.cleaned_data.get('DOB')
        age = datetime.datetime.now().year - DOB.year 
        student.age = age
        
    def save(self, commit=True):
        student = super().save(commit=False)
        self.name(student)
        self.dob(student)
        if commit:
            student.save()
        return student

    
       
class TeacherForm(ModelForm):
    class Meta:
        model = Supervisior
        fields = '__all__'
    
   

    def clean(self):
        cleaned_data = super().clean()
        fname = cleaned_data.get('fname')
        lname = cleaned_data.get('lname')
        address =cleaned_data.get('address')

        if Supervisior.objects.filter(fname=fname,lname=lname,address=address).exists():
            raise forms.ValidationError('Data already exists')


class FacultyForm(ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        
        if Faculty.objects.filter(name=name).exists():
            raise forms.ValidationError('Data already exists')


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        
        if Subject.objects.filter(name=name).exists():
            raise forms.ValidationError('Data already exists')