from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from .models import User,Student,Supervisior,Subject,Faculty
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def add_student(request):
    if request.method == 'POST':
        name = request.POST['name'].capitalize()
        age = request.POST['age']
        grade= request.POST['grade']
        address =request.POST['address'].capitalize()
        roll_no = request.POST['roll']
        supervisior = request.POST['supervisior'].capitalize()
        sup_address = request.POST['supervisior_add'].capitalize()
        faculty = request.POST['faculty'].capitalize()
        subject = request.POST['subject'].split(',')
        subject = [s.capitalize() for s in subject ]
        try:
            sup = Supervisior.objects.get(name=supervisior, address=sup_address)
        except Supervisior.DoesNotExist:
            sup = Supervisior(name=supervisior,address=address)
            sup.save()
        try:
            fac = Faculty.objects.get(name=faculty)
        except Faculty.DoesNotExist:
            fac = Faculty(name=faculty)
            fac.save()
        student = Student.objects.create(name=name,age=age,grade=grade,address=address,roll_no=roll_no,supervisior=sup,
        faculty=fac)
        student.save()
        for sub in subject:
            try:
                subj = Subject.objects.get(name=sub,faculty=fac)
            except Subject.DoesNotExist:
                subj = Subject(name=sub,faculty=fac)
                subj.save()
            student.subject.add(subj)

        return redirect(reverse('index'))
            
        

    else:

        return render(request,'student_management/add_student.html')

def search_student(request):
    if request.method == 'POST':
        name = request.POST['name'].capitalize()
        students = Student.objects.filter(name=name)
        return render(request,'student_management/index.html',{'students':students})
    else:
        return render(request,'student_management/search_student.html')


def update_student(request):
    if request.method == 'POST':
        name = request.POST['name'].capitalize()
        field = request.POST['field']
        value = request.POST['value']
        s = Student.objects.filter(name=name)[0]
        
        if s:
            setattr(s,'age', 100)
            s.save()
            return redirect(reverse('index'))
        else:
            return render(request,'student_management/update_student.html',{ 'message' :"No record to update"})

 
    else:

        return render (request,'student_management/update_student.html')

def delete_student(request):
    if request.method == 'POST':
        name = request.POST['name'].capitalize()
        student =  Student.objects.filter(name=name)
        if student:
            student.delete()
            return redirect(reverse('index'))
        else:
            return render(request,'student_management/delete_student.html',{"message":"No record to delete"})
    else:
        return render(request,'student_management/delete_student.html')


def index(request):
    students = Student.objects.all()
    return render(request,'student_management/index.html',{'students':students})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect(reverse('index'))

        else:
            return render(request, 'student_management/login.html',{
                'message':'Invalid username and/or password'
            })

    else:
        return render(request, 'student_management/login.html') 

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        conformation = request.POST['conformation']
        if password != conformation:
            return render(request,'student_management/layout.html',{'message':'password must match'})
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:

            return render(request,"student_management/register.html",{'message':'username already taken'})
        login(request, user)
        return redirect(reverse('index'))
    else:
        return render(request,"student_management/register.html")

