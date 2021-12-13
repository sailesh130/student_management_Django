from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from rest_framework.serializers import Serializer
from .models import CustomUser, Faculty, Student, Subject, Supervisior
from .serializers import StudentSeralizers,TeacherSeralizers,FacultySeralizers,SubjectSeralizers,RegisterSerializer,MyTokenObtainPairSerializer,ChangePasswordSerializer



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

    
class LogoutView(APIView):
   

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class ChangePasswordView(generics.UpdateAPIView):

    queryset = CustomUser.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer