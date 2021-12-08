from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from rest_framework.serializers import Serializer
from .models import Faculty, Student, Subject, Supervisior
from .serializers import StudentSeralizers,TeacherSeralizers,FacultySeralizers,SubjectSeralizers
import datetime

# Create your views here.

class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSeralizers
    filter_backends = [filters.SearchFilter]
    search_fields = ['fname','lname']
    ordering_fields = '__all__'
    ordering = ['fname','lname']

    def calculate_age(self,serializer):
        date = serializer.validated_data['DOB']
        today = datetime.datetime.now().year
        student_date = date.year 
        return  today - student_date



    def create(self, request, *args, **kwargs):
        serializer = StudentSeralizers(data = self.request.data)
        serializer.is_valid(raise_exception=True)
        age = self.calculate_age(serializer)
        serializer.save(age=age)
        return Response(status=status.HTTP_201_CREATED)
        
        

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSeralizers


class TeacherList(generics.ListCreateAPIView):
    queryset = Supervisior.objects.all()
    serializer_class = TeacherSeralizers

    def create(self, request, *args, **kwargs):
        serializer = TeacherSeralizers(data = self.request.data)
        serializer.is_valid(raise_exception=True)
        f_name = serializer.validated_data['fname']
        l_name = serializer.validated_data['lname']
        teacher_address = serializer.validated_data['address']
        obj, created = Supervisior.objects.get_or_create(fname=f_name,lname=l_name,address=teacher_address)
        if obj:
            
            return Response(status=status.HTTP_409_CONFLICT)

        else:
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)


class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supervisior.objects.all()
    serializer_class = TeacherSeralizers

    


class FacultyList(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySeralizers

    def create(self, request, *args, **kwargs):
        serializer = FacultySeralizers(data = self.request.data)
        serializer.is_valid(raise_exception=True)
        faculty_name = serializer.validated_data['name']
        teacher = serializer.validated_data['teacher']
        subject = serializer.validated_data['teacher']
        obj, created = Faculty.objects.get_or_create(name=faculty_name)
        if obj:
            return Response(status=status.HTTP_409_CONFLICT)

        else:
            serializer.save(teacher=teacher,subject=subject)
            return Response(status=status.HTTP_201_CREATED)
            


class FacultyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySeralizers


class SubjectList(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSeralizers


    def create(self, request, *args, **kwargs):
        serializer = SubjectSeralizers(data = self.request.data)
        serializer.is_valid(raise_exception=True)
        subject_name = serializer.validated_data['name']
        teacher = serializer.validated_data['teacher']
        obj, created = Subject.objects.get_or_create(name=subject_name)

        if obj:
            return Response(status=status.HTTP_409_CONFLICT)

        else:
            serializer.save(teacher=teacher)
            return Response(status=status.HTTP_201_CREATED)
            


class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSeralizers

    