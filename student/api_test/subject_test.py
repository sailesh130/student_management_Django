from datetime import date, datetime
from django.urls import reverse_lazy
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from ..models import CustomUser, Faculty, Student, Subject,Supervisior
from rest_framework.test import force_authenticate
import json
from PIL import Image


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