from rest_framework import serializers
from .models import Student,Supervisior,Subject,Faculty


class StudentSeralizers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        
        model = Student


        
class TeacherSeralizers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        
        model = Supervisior

class FacultySeralizers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        
        model = Faculty

class SubjectSeralizers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
       
        model = Subject