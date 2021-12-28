from datetime import date, datetime
from django.urls import reverse_lazy
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from .models import CustomUser, Faculty, Student, Subject,Supervisior
from rest_framework.test import force_authenticate
import json
from rest_framework.test import APIClient


register_data = {
                    "username": "testuser",
                    "email": "testuser@gmail.com",
                    "password1": "python123",
                    "password2": "python123"
                }

register_url = '/api/register/'

login_data = {
                        "email": "testuser@gmail.com",
                        "password": "python123"
            }

login_url = '/api/login/'

class UserTests(APITestCase):

    def setUp(self):
        super().setUp()
        self.data = {
                    "username": "testuser1",
                    "email": "testuser1@gmail.com",
                    "password1": "python123",
                    "password2": "python123"
                    }
        self.url = '/api/register/'

        self.register = self.client.post(register_url, register_data)
        self.login = self.client.post(login_url, login_data,format='json')
        self.token = self.login.data['access']
        self.user = CustomUser.objects.get(username='testuser')

    
            
    def test_create_user(self):
        """
        Ensure we can create a new account object.
        """
        print("Registraing user")
        response= self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(username="testuser1").email, 'testuser1@gmail.com')
        
    def test_login(self):
        print("Logging User")
        url = '/api/login/'

        data = {
                        "email": "testuser@gmail.com",
                        "password": "python123"
                    }
        register = self.client.post(url,data,format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    
class TeacherTests(APITestCase):

    def setUp(self): 

        super().setUp()
        self.teacher = Supervisior.objects.create(fname="Ram",lname= "Bhadur",address= "Pok")
        self.url = reverse('teacher')
        self.register = self.client.post(register_url, register_data)
        self.login = self.client.post(login_url, login_data,format='json')
        self.token = self.login.data['access']
        self.user = CustomUser.objects.get(username='testuser')


        

    def test_create_teacher(self):
        print("Creating teacher")
        data = {
            "fname":"Sita",
            "lname":"Rita",
            "address":"Kathmandu"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Supervisior.objects.count(),2)
        self.assertEqual(Supervisior.objects.get(fname='Sita').fname,'Sita')
        
       

    def test_details_teacher(self):
        print("Searching teacher details")
        url = reverse('teacher_details', args=[self.teacher.pk])
        response = self.client.get(url,format='json')
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data['fname'],'Ram')


    def test_teacher_list(self):
        print("Searching teacher list")
        url = reverse("teacher")
        response = self.client.get(url,format='json')
        data = json.loads(response.content)
        self.assertEqual(data[0]['fname'],"Ram")
        
        
    def test_teacher_update(self):
        print("Updating teacher")

        url = reverse('teacher_details', args=[self.teacher.pk])
        data = {
            
            "address": "USA"

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.patch(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['address'],'USA')

    def test_teacher_delete(self):
        print("Deleting teacher")
        url = reverse('teacher_details', args=[self.teacher.pk])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        

    def test_not_found(self):
        print("Checking for teacher without entry in database")
        url = reverse('teacher_details',kwargs={'pk':100})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

class SubjectTests(APITestCase):

    def setUp(self):
        super().setUp()
        self.teacher = Supervisior.objects.create(fname="Ram",lname= "Bhadur",address= "Pok")
        self.subject = Subject.objects.create(name='English')
        self.subject.teacher.add(self.teacher)
        self.url = reverse('subject')
        self.url_details = reverse('subject_details',args=[self.subject.pk])
        self.register = self.client.post(register_url, register_data)
        self.login = self.client.post(login_url, login_data,format='json')
        self.token = self.login.data['access']
        self.user = CustomUser.objects.get(username='testuser')

        

    def test_create_subject(self):
        print("Creating subject")
        data = {
            "name":"Nepali",
            "teacher": [self.teacher.pk]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Subject.objects.count(),2)
        self.assertEqual(Subject.objects.get(name='Nepali').name,'Nepali')


    def test_details_subject(self):
        print("Searching subject details")
        response = self.client.get(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['name'],'English')


    def test_subject_list(self):
        print("Searching subject list")
        response = self.client.get(self.url,format='json')
        data = response.data
        self.assertEqual(data[0]['name'],"English")


    def test_teacher_update(self):
        print("Updating teacher")        
        data = {
            
            "name": "Biology"

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.patch(self.url_details,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['name'],'Biology')


    def test_subject_delete(self):
        print("Deleting subject")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_not_found(self):
        print("Checking subject without database entry exists")
        url = reverse('subject_details',kwargs={'pk':100})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


class FacultyTests(APITestCase):

    def setUp(self):
        super().setUp()
        
        self.teacher = Supervisior.objects.create(fname="Ram",lname= "Bhadur",address= "Pok")
        self.subject = Subject.objects.create(name='English')
        self.subject.teacher.add(self.teacher)
        self.faculty = Faculty.objects.create(name='Science')
        self.faculty.teacher.add(self.teacher)
        self.faculty.subject.add(self.subject)
        self.url = reverse('faculty')
        self.url_details = reverse('faculty_details',args=[self.faculty.pk])
        self.register = self.client.post(register_url, register_data)
        self.login = self.client.post(login_url, login_data,format='json')
        self.token = self.login.data['access']
        self.user = CustomUser.objects.get(username='testuser')
        

    def test_create_faculty(self):
        print("Creating faculty")
        data = {
            "name":"Management",
            "teacher": [self.teacher.pk],
            "subject":[self.subject.pk]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Faculty.objects.count(),2)
        self.assertEqual(Faculty.objects.get(name='Management').name,'Management')


    def test_details_faculty(self):
        print("Searching faculty details")
        response = self.client.get(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['name'],'Science')


    def test_teacher_list(self):
        print("Searching teacher list")
        response = self.client.get(self.url,format='json')
        data = response.data
        self.assertEqual(data[0]['name'],"Science")


    def test_faculty_update(self):
        print("Updating faculty")

        
        data = {
            
            "name": "Arts"

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.patch(self.url_details,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['name'],'Arts')


    def test_faculty_delete(self):
        print("Deleting faculty")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_not_found(self):
        print("Checking faculty without database entry exists")
        url = reverse('faculty_details',kwargs={'pk':100})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)



class StudentTests(APITestCase):

    def setUp(self):
        super().setUp()
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
        self.register = self.client.post(register_url, register_data)
        self.login = self.client.post(login_url, login_data,format='json')
        self.token = self.login.data['access']
        self.user = CustomUser.objects.get(username='testuser')

        

    def test_create_student(self):
        print("Creating student")

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

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(),2)
        self.assertEqual(Student.objects.get(email='kumari@gmail.com').fname,'Kumari')

    
    def test_details_student(self):
        print("Searching student details")
        response = self.client.get(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['email'],'hari@gmail.com')


    def test_student_list(self):
        print("Searching student list")
        response = self.client.get(self.url,format='json')
        data = response.data
        self.assertEqual(data[0]['email'],"hari@gmail.com")


    def test_student_update(self):
        print("Updating student")

        
        data = {
            
            "email": "haribhadur@gmail.com"

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.patch(self.url_details,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['email'],'haribhadur@gmail.com')


    def test_student_delete(self):
        print("Deleting student")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(self.url_details,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_not_found(self):
        print("Checking student without database entry exists")
        url = reverse('student_details',kwargs={'pk':100})
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


    



            


        
            
