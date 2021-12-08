from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from rest_framework.serializers import Serializer
from .models import Faculty, Student, Subject, Supervisior
from .serializers import StudentSeralizers,TeacherSeralizers,FacultySeralizers,SubjectSeralizers


# Create your views here.

class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSeralizers
    filter_backends = [filters.SearchFilter]
    search_fields = ['fname','lname']
    ordering_fields = '__all__'
    ordering = ['fname']

        

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSeralizers


class TeacherList(generics.ListCreateAPIView):
    queryset = Supervisior.objects.all()
    serializer_class = TeacherSeralizers

    



class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supervisior.objects.all()
    serializer_class = TeacherSeralizers

    


class FacultyList(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySeralizers

    


class FacultyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySeralizers


class SubjectList(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSeralizers


    
            
class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSeralizers

    