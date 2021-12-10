from datetime import date, datetime
from django.urls import reverse_lazy
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from .models import CustomUser, Faculty, Student, Subject,Supervisior
from rest_framework.test import force_authenticate
import json
from PIL import Image



class UserTests(APITestCase):
     
    def test_create_user(self):
        """
        Ensure we can create a new account object.
        """
        url = '/api/rest-auth/registration/'
        
        data = {
                    "username": "test",
                    "email": "test@gmail.com",
                    "password1": "python123",
                    "password2": "python123"
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'test@gmail.com')
        

    def test_login(self):
        url = '/api-auth/login/'

        data = {
                        "email": "test@gmail.com",
                        "password": "python123"
                    }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    
class TeacherTests(APITestCase):

    def setUp(self): 

        super().setUp()
        self.user = CustomUser.objects.create(username="test",email="test@gmail.com",password="python123")
        self.teacher = Supervisior.objects.create(fname="Ram",lname= "Bhadur",address= "Pok")
        self.url = reverse('teacher')
       

    def test_create_teacher(self):
        data = {
            "fname":"Sita",
            "lname":"Rita",
            "address":"Kathmandu"
        }
        self.client.force_login(self.user)
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Supervisior.objects.count(),2)
        self.assertEqual(Supervisior.objects.get(fname='Sita').fname,'Sita')
        
       

    def test_details_teacher(self):
        url = reverse('teacher_details', args=[self.teacher.pk])
        response = self.client.get(url,format='json')
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data['fname'],'Ram')


    def test_teacher_list(self):
        url = reverse("teacher")
        response = self.client.get(url,format='json')
        data = json.loads(response.content)
        self.assertEqual(data[0]['fname'],"Ram")
        
        
    def test_teacher_update(self):

        url = reverse('teacher_details', args=[self.teacher.pk])
        data = {
            
            "address": "USA"

        }

        self.client.force_login(self.user)
        response = self.client.patch(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['address'],'USA')

    def test_teacher_delete(self):
        url = reverse('teacher_details', args=[self.teacher.pk])
        self.client.force_login(self.user)
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        

    def test_not_found(self):
        url = reverse('teacher_details',kwargs={'pk':100})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

class SubjectTests(APITestCase):

    def setUp(self):
        super().setUp()
        
        self.user = CustomUser.objects.create(username="test",email="test@gmail.com",password="python123")
        self.teacher = Supervisior.objects.create(fname="Ram",lname= "Bhadur",address= "Pok")
        self.subject = Subject.objects.create(name='English')
        self.subject.teacher.add(self.teacher)
        self.url = reverse('subject')
        self.url_details = reverse('subject_details',args=[self.subject.pk])
        

    def test_create_subject(self):
        data = {
            "name":"Nepali",
            "teacher": [self.teacher.pk]
        }
        self.client.force_login(self.user)
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Subject.objects.count(),2)
        self.assertEqual(Subject.objects.get(name='Nepali').name,'Nepali')


    def test_details_subject(self):
        response = self.client.get(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['name'],'English')


    def test_teacher_list(self):
        response = self.client.get(self.url,format='json')
        data = response.data
        self.assertEqual(data[0]['name'],"English")


    def test_teacher_update(self):

        
        data = {
            
            "name": "Biology"

        }

        self.client.force_login(self.user)
        response = self.client.patch(self.url_details,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['name'],'Biology')


    def test_teacher_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_not_found(self):
        url = reverse('subject_details',kwargs={'pk':100})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


class FacultyTests(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = CustomUser.objects.create(username="test",email="test@gmail.com",password="python123")
        self.teacher = Supervisior.objects.create(fname="Ram",lname= "Bhadur",address= "Pok")
        self.subject = Subject.objects.create(name='English')
        self.subject.teacher.add(self.teacher)
        self.faculty = Faculty.objects.create(name='Science')
        self.faculty.teacher.add(self.teacher)
        self.faculty.subject.add(self.subject)
        self.url = reverse('faculty')
        self.url_details = reverse('faculty_details',args=[self.faculty.pk])
        

    def test_create_faculty(self):
        data = {
            "name":"Management",
            "teacher": [self.teacher.pk],
            "subject":[self.subject.pk]
        }
        self.client.force_login(self.user)
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Faculty.objects.count(),2)
        self.assertEqual(Faculty.objects.get(name='Management').name,'Management')


    def test_details_faculty(self):
        response = self.client.get(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['name'],'Science')


    def test_teacher_list(self):
        response = self.client.get(self.url,format='json')
        data = response.data
        self.assertEqual(data[0]['name'],"Science")


    def test_teacher_update(self):

        
        data = {
            
            "name": "Arts"

        }

        self.client.force_login(self.user)
        response = self.client.patch(self.url_details,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['name'],'Arts')


    def test_teacher_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_not_found(self):
        url = reverse('faculty_details',kwargs={'pk':100})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)



class SubjectTests(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = CustomUser.objects.create(username="test",email="test@gmail.com",password="python123")
        self.teacher = Supervisior.objects.create(fname="Ram",lname= "Bhadur",address= "Pok")
        self.subject = Subject.objects.create(name='English')
        self.subject.teacher.add(self.teacher)
        self.url = reverse('subject')
        self.url_details = reverse('subject_details',args=[self.subject.pk])
        

    def test_create_subject(self):
        data = {
            "name":"Nepali",
            "teacher": [self.teacher.pk]
        }
        self.client.force_login(self.user)
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Subject.objects.count(),2)
        self.assertEqual(Subject.objects.get(name='Nepali').name,'Nepali')


    def test_details_subject(self):
        response = self.client.get(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['name'],'English')


    def test_teacher_list(self):
        response = self.client.get(self.url,format='json')
        data = response.data
        self.assertEqual(data[0]['name'],"English")


    def test_teacher_update(self):

        
        data = {
            
            "name": "Biology"

        }

        self.client.force_login(self.user)
        response = self.client.patch(self.url_details,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['name'],'Biology')


    def test_teacher_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_not_found(self):
        url = reverse('subject_details',kwargs={'pk':100})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


class StudentTests(APITestCase):

    def setUp(self):
        super().setUp()
        self.photo = Image.open('/home/sapkota/Pictures/Screenshots/Screenshot from 2021-12-06 21-17-50.png')
        self.user = CustomUser.objects.create(username="test",email="test@gmail.com",password="python123")
        self.teacher = Supervisior.objects.create(fname="Ram",lname= "Bhadur",address= "Pok")
        self.subject = Subject.objects.create(name='English')
        self.subject.teacher.add(self.teacher)
        self.faculty = Faculty.objects.create(name='Science')
        self.faculty.teacher.add(self.teacher)
        self.faculty.subject.add(self.subject)
        self.student = Student.objects.create(fname='Hari',lname='kumar',
        address = 'Pokhara',email = 'hari@gmail.com',DOB='1998-10-01',
        grade = 12,roll_no= 123,faculty=self.faculty)
        self.url = reverse('student')
        self.url_details = reverse('student_details',args=[self.student.pk])
        

    def test_create_student(self):

        data = {
                    "fname": "Kumari",
                    "lname": "Kanxa",
                    "address": "Pokhara",
                    "email": "kumari@gmail.com",
                    "DOB": '1999-11-12',
                    "grade": 12,
                    "roll_no": 133,
                    "faculty": self.faculty.pk
                }

        self.client.force_login(self.user)
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(),2)
        self.assertEqual(Student.objects.get(email='kumari@gmail.com').fname,'Kumari')

    
    def test_details_student(self):
        response = self.client.get(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['email'],'hari@gmail.com')


    def test_student_list(self):
        response = self.client.get(self.url,format='json')
        data = response.data
        self.assertEqual(data[0]['email'],"hari@gmail.com")


    def test_student_update(self):

        
        data = {
            
            "email": "haribhadur@gmail.com"

        }

        self.client.force_login(self.user)
        response = self.client.patch(self.url_details,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['email'],'haribhadur@gmail.com')


    def test_student_delete(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_not_found(self):
        url = reverse('student_details',kwargs={'pk':100})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


    



            


        
            
