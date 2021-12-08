from rest_framework import serializers
from .models import Student,Supervisior,Subject,Faculty
import datetime

class StudentSeralizers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        
        model = Student

    def calculate_age(self,validated_data):
        date = validated_data['DOB']
        today = datetime.datetime.now().year
        student_date = date.year 
        return  today - student_date

    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        age = self.calculate_age(validated_data)
        student.age = age
        student.save()
        return student

     
class TeacherSeralizers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        
        model = Supervisior

    def create(self,validated_data):
        teacher,created = Supervisior.objects.get_or_create(**validated_data)
        if not created:
            raise serializers.ValidationError("Teacher already exists")

        return teacher
        

class FacultySeralizers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Faculty

    def validate_name(self,name):
        faculty = Faculty.objects.filter(name=name).exists()
        if  faculty:
            raise serializers.ValidationError("Faculty already exists")

        return name

        
class SubjectSeralizers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Subject

    def validate_name(self,name):
        subject = Subject.objects.filter(name=name).exists()
        if  subject:
            raise serializers.ValidationError("Subject already exists")

        return name

        