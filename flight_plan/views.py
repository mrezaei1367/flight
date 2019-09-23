import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from base.pagination import BasePagination
from .models import Flight
from base.views import BaseModelViewset
from .serializers import FlightSerializer
from .utils import search_flight

error_logger = logging.getLogger('error_logger')


class FlightViewSet(BaseModelViewset):
    permission_classes = [IsAuthenticated]
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()
    pagination_class = BasePagination

    def list(self, request, *args, **kwargs):
        try:
            flight_name = request.GET.get('flight_name')
            scheduled_date = request.GET.get('scheduled_date')
            departure = request.GET.get('departure')
            destination = request.GET.get('destination')
            queryset = self.get_queryset()
            queryset = search_flight(queryset, flight_name, departure, destination, scheduled_date)
            page = self.paginate_queryset(queryset)
            serializer = FlightSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            errs = {'errors': [{
                'status': 400,
                'detail': str(e),
                'source': {'pointer': request.path}
            }]}
            error_logger.error({'response': errs})
            return Response(errs, status.HTTP_400_BAD_REQUEST)
