from rest_framework.serializers import ModelSerializer
from .models import Flight
from base.serializers import ErrorHandlerSerializerMixin


class FlightSerializer(ModelSerializer, ErrorHandlerSerializerMixin):
    class Meta:
        model = Flight
        fields = [
            'id',
            'flight_name',
            'flight_number',
            'scheduled_date',
            'expected_arrival_date',
            'departure',
            'destination',
            'flight_duration',
            'fare',
        ]
