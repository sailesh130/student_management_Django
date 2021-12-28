from datetime import date, datetime
from django.urls import reverse_lazy
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from ..models import CustomUser, Faculty, Student, Subject,Supervisior
from rest_framework.test import force_authenticate
import json
from PIL import Image


class UserTests(APITestCase):
     
    def test_create_user(self):
        """
        Ensure we can create a new account object.
        """
        url = '/api/register/'
        
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
        url = '/api/login/'

        data = {
                        "email": "test@gmail.com",
                        "password": "python123"
                    }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
