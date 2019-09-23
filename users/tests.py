from users.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.sign_up_url = reverse('signup')
        self.user_profile_url = reverse('profile')
        self.data = {
            "username": "testuser2",
            "password": "somepassword",
            "re_password": "somepassword",
            "address": "tehran",
            "mobile_number": "09128122752",
            "first_name": "Mohammad",
            "last_name": "Rezaei",
            "birth_date": "1988-09-20",
            "birth_place": "Tehran",
            "email": "test@yahoo.com"
        }

    def test_get_user_profile(self):
        response = self.client.post(self.sign_up_url, self.data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.data['username'])
        self.token = 'JWT ' + response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.data['username'])
