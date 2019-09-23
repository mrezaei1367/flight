from django.urls import reverse
from rest_framework import status
from rest_framework.test import (APITestCase,
                                 APIRequestFactory)
from .models import Flight
from .views import FlightViewSet


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
        self.flight_data = {
            "flight_name": "ILKST",
            "flight_number": "HTgG645",
            "scheduled_date": "2019-10-25T00:00:00Z",
            "expected_arrival_date": "2019-10-25T15:00:00Z",
            "departure": "Tehran",
            "destination": "Istanbul",
            "flight_duration": "6:30",
            "fare": 2230000.0
        }

        self.factory = APIRequestFactory()
        self.sign_up_url = reverse('signup')
        response = self.client.post(self.sign_up_url, self.data, format='json')
        self.token = 'JWT ' + response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        self.flight_url = reverse('flight-list')

    def test_add_flight(self):
        response = self.client.post(self.flight_url, self.flight_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flight.objects.count(), 1)

    def test_get_flight_list(self):
        response = self.client.post(self.flight_url, self.flight_data)
        response = self.client.get(self.flight_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Flight.objects.count(), 1)

    def test_retrieve_flight(self):
        response = self.client.post(self.flight_url, self.flight_data)
        request = self.factory.get("/flight", HTTP_AUTHORIZATION=self.token)
        flight_detail = FlightViewSet.as_view({'get': 'retrieve'})
        response = flight_detail(request, pk=response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_flight(self):
        response = self.client.post(self.flight_url, self.flight_data)
        request = self.factory.put("/flight", HTTP_AUTHORIZATION=self.token)
        flight_detail = FlightViewSet.as_view({'put': 'update'})
        response = flight_detail(request, pk=response.data["id"], data=self.flight_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_flight_right_params(self):
        params = {
            "departure": "Tehran",
            "flight_name": "ILKST",
            "scheduled_date": "2019-10-25",
            "destination": "Istanbul"
        }
        response = self.client.post(self.flight_url, self.flight_data)
        response = self.client.get(self.flight_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), Flight.objects.count())

    def test_search_flight_wrong_departure_params(self):
        params = {
            "departure": "Shikago",
        }
        response = self.client.post(self.flight_url, self.flight_data)
        response = self.client.get(self.flight_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_search_flight_wrong_flight_name_params(self):
        params = {
            "flight_name": "IKL",
        }
        response = self.client.post(self.flight_url, self.flight_data)
        response = self.client.get(self.flight_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_search_flight_wrong_destination_params(self):
        params = {
            "destination": "Iska",
        }
        response = self.client.post(self.flight_url, self.flight_data)
        response = self.client.get(self.flight_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_search_flight_wrong_scheduled_date_params(self):
        params = {
            "scheduled_date": "2019-10-29",
        }
        response = self.client.post(self.flight_url, self.flight_data)
        response = self.client.get(self.flight_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
