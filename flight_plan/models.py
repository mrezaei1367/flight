from django.db import models
from base.models import Base


class Flight(Base):
    flight_name = models.CharField(max_length=200, null=True, blank=True, db_index=True)
    flight_number = models.CharField(null=True, blank=True, max_length=20, unique=True)
    scheduled_date = models.DateTimeField(db_index=True, editable=True, blank=True)
    expected_arrival_date = models.DateTimeField(editable=True, blank=True)
    destination = models.CharField(max_length=200, null=True, blank=True, db_index=True)
    departure = models.CharField(max_length=200, null=True, blank=True, db_index=True)
    fare = models.FloatField(null=True, blank=True)
    flight_duration = models.CharField(max_length=10, null=True, blank=True)
