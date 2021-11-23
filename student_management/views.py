from django.shortcuts import render,redirect
from django.urls import reverse
from .models import User,Student,Supervisior,Subject,Faculty
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .forms import AddStudent, RegisterForm,UpdateStudent
# Create your views here.
def add_student(request):
    if request.method == 'POST':
        form = AddStudent(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].capitalize()
            age = form.cleaned_data['age']
            grade= form.cleaned_data['grade']
            address =form.cleaned_data['address'].capitalize()
            roll_no = form.cleaned_data['roll_no']
            supervisior = form.cleaned_data['supervisior'].capitalize()
            sup_address = form.cleaned_data['supervisior_add'].capitalize()
            faculty = form.cleaned_data['faculty'].capitalize()
            subject = form.cleaned_data['subject']
            
            subject = [s.capitalize() for s in subject ]

            record,sup = Supervisior.objects.get_or_create(name=supervisior, address=sup_address)
            if record:
                supervisior = record
            else:
                supervisior = sup
                sup.save()
               
            fac_record , fact =Faculty.objects.get_or_create(name=faculty)
            if fac_record:
                fac = fac_record
            else:
                fac= fact
                fact.save()
            print(sup)  
            student = Student.objects.create(name=name,age=age,grade=grade,address=address,roll_no=roll_no,supervisior=supervisior,
            faculty=fac)
            student.save()
            
            for sub in subject:
                sub_record,subject = Subject.objects.get_or_create(name=sub,faculty=fac)
                if sub_record:
                    subj = sub_record
                else:
                    subject.save()
                    subj = subject
                student.subject.add(subj)

            return redirect(reverse('index'))
        else:
            return render(request,'student_management/add_student.html',{'form':form})


            
    else:
        form = AddStudent()

        return render(request,'student_management/add_student.html',{'form':form})

def search_student(request):
    if request.method == 'POST':
        name = request.POST['name'].capitalize()
        students = Student.objects.filter(name=name)
        return render(request,'student_management/index.html',{'students':students})
    else:
        return render(request,'student_management/search_student.html')



def update_student(request):
    if request.method == 'POST':
        form = UpdateStudent(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].capitalize()
            field = form.cleaned_data['field']
            value = form.cleaned_data['value']
        try:
            s = Student.objects.get(name=name)
        except:
            form = UpdateStudent()
            return render(request,'student_management/update_student.html',{ 'message' :"No record to update",'form':form})

        if field == 'supervisior':
            form = UpdateStudent()
            return render(request,'student_management/update_student.html',{ 'message' :"cannot update supervisior field",'form':form})
        elif field =='faculty':
            form = UpdateStudent()
            return render(request,'student_management/update_student.html',{ 'message' :"cannot update supervisior field",'form':form})

        else:
            value = int(value)
            
        if s:
            setattr(s,field, value)
            s.save()
            return redirect(reverse('index'))
        
    else:
        form = UpdateStudent()
        return render (request,'student_management/update_student.html',{'form':form})


def delete_student(request):
    if request.method == 'POST':
        name = request.POST['name'].capitalize()
        try:
            student =  Student.objects.get(name=name)
            student.delete()
            return redirect(reverse('index'))
        except:
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
    return redirect(reverse('index'))



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name'].capitalize()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            conformation = form.cleaned_data['conformation']
            
            if password != conformation:
                form = RegisterForm()
                return render(request,'student_management/register.html',{'message':'password must match','form':form})
        
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                form = RegisterForm()
                return render(request,"student_management/register.html",{'message':'username already taken','form':form})
            login(request, user)
            return redirect(reverse('index'))

    else:
        form = RegisterForm()
        return render(request,"student_management/register.html",{'form':form})

