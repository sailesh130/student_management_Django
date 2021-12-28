from datetime import date, datetime
from django.urls import reverse_lazy
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from ..models import CustomUser, Faculty, Student, Subject,Supervisior
from rest_framework.test import force_authenticate
import json
from PIL import Image

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

