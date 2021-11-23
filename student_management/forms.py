from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django.core.validators import MaxValueValidator, MinValueValidator

class People(forms.Form):
    name = forms.CharField(label="student name",min_length=3,max_length=100)
    class Meta:
        abstract = True


class RegisterForm( People,forms.Form):
    
    email = forms.EmailField(label="email",max_length=254)
    password = password = forms.CharField(label="password",widget=forms.PasswordInput)
    conformation = forms.CharField(label="conformation",widget=forms.PasswordInput)


class AddStudent( People,forms.Form):
    
    age = forms.IntegerField(label="student age",validators=[MinValueValidator(1)])
    grade = forms.IntegerField(label="grade",validators=[MinValueValidator(1),MaxValueValidator(12)])
    address = forms.CharField(label="address",min_length=3,max_length=100,error_messages = {
                 'exceed':'Number of character cannot exceed 100'})
    roll_no = forms.IntegerField(label="roll_no",validators=[MinValueValidator(1)])
    supervisior = forms.CharField(label='supervisior name',min_length=3,max_length=100)
    supervisior_add = forms.CharField(label='supervisor address',min_length=3,max_length=100)
    faculty = forms.CharField(label='faculty name',min_length=3,max_length=100)
    subject =  SimpleArrayField(forms.CharField(label="subject",max_length=100,min_length=3))


class UpdateStudent( People, forms.Form):
    field = forms.CharField(label='field name',max_length=100,
    error_messages = {
                 'exceed':'Number of character cannot exceed 100'})
    value = forms.CharField(label='field value',max_length=100,
    error_messages = {
                 'exceed':'Number of character cannot exceed 100'})



