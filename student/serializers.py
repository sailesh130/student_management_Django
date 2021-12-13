from rest_framework import serializers
from .models import CustomUser, Student,Supervisior,Subject,Faculty
import datetime
from drf_braces.serializers.form_serializer import FormSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .forms import CustomUserCreateForm

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


class RegisterSerializer(FormSerializer):
    class Meta:
        form = CustomUserCreateForm


    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token 


class ChangePasswordSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password1', 'password2')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password1'])
        instance.save()

        return instance