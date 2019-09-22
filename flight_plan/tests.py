from users.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Flight



class Flight_planTest(APITestCase):


    def setUp(self):
        self.data = {
            "username": "flightuser",
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
        self.sign_up_url = reverse('signup')
        response = self.client.post(self.sign_up_url, self.data, format='json')
        self.token=response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
        # URL for flight
        self.flight_url = reverse('flight-list')
        # self.flight_detail_url = reverse('flight-detail')
        self.ADD_FLIGHT_METHOD="POST"
        self.UPDATE_FLIGHT_METHOD="PUT"
        self.LIST_FLIGHT_METHOD="GET"
        self.DELETE_FLIGHT_METHOD="DELETE"

    def test_add_flight(self):
        data={
            "flight_name": "IST",
            "flight_number": "HTgG645",
            "scheduled_date": "2019-10-25T00:00:00Z",
            "expected_arrival_date": "2019-10-25T15:00:00Z",
            "departure": "Tehran",
            "destination": "Istanbul",
            "flight_duration": "6:30",
            "fare": 2230000.0
        }

        response = self.client.post(self.flight_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flight.objects.count(), 1)

    def test_get_list(self):
        response = self.client.get(self.flight_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_flight(self):
        data = {
            "flight_name": "IGST",
            "flight_number": "2HTgG645",
            "scheduled_date": "2019-10-25T00:00:00Z",
            "expected_arrival_date": "2019-10-25T15:00:00Z",
            "departure": "Tehran",
            "destination": "Istanbul",
            "flight_duration": "5:30",
            "fare": 4230000.0
        }
        response = self.client.post(self.flight_url, data)
        response = self.client.get(reverse('flight-detail',args=(response.data["id"])))
        self.assertEqual(response.status_code, status.HTTP_200_OK)