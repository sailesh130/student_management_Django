from datetime import date, datetime
from django.urls import reverse_lazy
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from ..models import CustomUser, Faculty, Student, Subject,Supervisior
from rest_framework.test import force_authenticate
import json
from PIL import Image


   
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
