from users.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.conf import settings


class AuthenticationTest(APITestCase):


    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser', 'testpassword')

        # URL for creating an account.
        self.sign_up_url = reverse('signup')
        # self.sign_up_url = 'http://127.0.0.1:8000/api/v1/auth/signup/'
        # URL for log in
        self.log_in_url = reverse('login')
        # self.log_in_url = 'http://127.0.0.1:8000/api/v1/auth/login/'



    def test_register_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            "username": "testuser2",
            "password": "somepassword",
            "re_password":"somepassword",
            "address": "tehran",
            "mobile_number": "09128122752",
            "first_name": "Mohammad",
            "last_name": "Rezaei",
            "birth_date": "1988-09-20",
            "birth_place": "Tehran",
            "email": "test@yahoo.com"
        }

        response = self.client.post(self.sign_up_url, data, format='json')

        # We want to make sure we have two users in the database..
        self.assertEqual(User.objects.count(), 2)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertFalse('password' in response.data)
