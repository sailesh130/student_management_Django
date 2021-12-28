from datetime import date, datetime
from django.urls import reverse_lazy
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from ..models import CustomUser, Faculty, Student, Subject,Supervisior
from rest_framework.test import force_authenticate
import json
from PIL import Image

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


    
