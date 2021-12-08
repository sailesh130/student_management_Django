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

    def create(self, validated_data):
        obj,teacher = Supervisior.objects.get_or_create(**validated_data)
        if obj:
            teacher = Supervisior.objects.get(pk=obj.pk)
            return teacher
        else:
           
            return teacher
            

class FacultySeralizers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        
        model = Faculty

        def create(self, validated_data):
            name = validated_data['name']
            teacher = validated_data['teacher']
            subject = validated_data['subject']

            obj, faculty = Faculty.objects.get_or_create(name = name)
            if obj:
                raise serializers.ValidationError("Faculty already exists")

            else:
                faculty.teacher = teacher
                faculty.subject = subject
                faculty.save()
                return faculty
            

class SubjectSeralizers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
       
        model = Subject

        def create(self, validated_data):
            name = validated_data['name']
            teacher = validated_data['teacher']

            obj, subject = Subject.objects.get_or_create(name = name)
            if obj:
                raise serializers.ValidationError("Subject already exists")

            else:
                subject.teacher = teacher
                subject.save()
                return subject