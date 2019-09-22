from users.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import TokenByIPPayload



class AuthenticationTest(APITestCase):


    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user(username='testuser', password='testpassword',email='test@yahoo.com')

        # URL for creating an account.
        self.sign_up_url = reverse('signup')
        # URL for log in
        self.log_in_url = reverse('login')
        self.data = {
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


    def test_register_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """

        response = self.client.post(self.sign_up_url, self.data, format='json')

        # We want to make sure we have two users in the database..
        self.assertEqual(User.objects.count(), 2)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.data['username'])
        self.assertFalse('password' in response.data)

    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        self.data["username"]="foobar"
        self.data["password"]="foo"
        self.data["re_password"]="foo"

        response = self.client.post(self.sign_up_url, self.data, format='json')
        user = User.objects.latest('id')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        token_count = TokenByIPPayload.objects.filter(user=user).count()
        self.assertEqual(token_count, 0)

    def test_create_user_with_no_password(self):

        self.data["username"] = "foobar"
        self.data["password"] = ""
        self.data["re_password"] = ""
        response = self.client.post(self.sign_up_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_with_too_long_username(self):

        self.data["username"] = "foo" * 30
        self.data["password"] = "12345678"
        self.data["re_password"] = "12345678"

        response = self.client.post(self.sign_up_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_with_no_username(self):
        self.data["username"] = ""
        self.data["password"] = "12345678"
        self.data["re_password"] = "12345678"

        response = self.client.post(self.sign_up_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_with_preexisting_username(self):

        self.data["username"] = "testuser"
        self.data["password"] = "12345678"
        self.data["re_password"] = "12345678"

        response = self.client.post(self.sign_up_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def wrong_password_attempts_by_username(self):

        self.data["username"] = "wronuser"
        self.data["password"] = "12345678"
        self.data["re_password"] = "12345678"

        response = self.client.post(self.sign_up_url, self.data, format='json')
        self.data["password"]="87654321"
        response = self.client.post(self.log_in_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)