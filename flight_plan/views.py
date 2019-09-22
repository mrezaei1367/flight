import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from base.pagination import BasePagination
from .models import Flight
from base.views import BaseModelViewset
from .serializers import FlightSerializer


error_logger = logging.getLogger('error_logger')


class FlightViewSet(BaseModelViewset):
    permission_classes = [IsAuthenticated]
    serializer_class=FlightSerializer
    queryset = Flight.objects.all()
    pagination_class = BasePagination

    def list(self, request, *args, **kwargs):
        try:
            flight_name = request.GET.get('flight_name')
            scheduled_date = request.GET.get('scheduled_date')
            departure = request.GET.get('departure')
            destination = request.GET.get('destination')
            queryset=self.get_queryset()
            if flight_name:
                queryset =queryset.filter(flight_name__icontains=flight_name)
            if departure:
                queryset=queryset.filter(departure__icontains=departure)
            if destination:
                queryset=queryset.filter(destination__icontains=destination)
            if scheduled_date:
                queryset=queryset.filter(scheduled_date=scheduled_date)
            queryset=queryset.order_by('scheduled_date')
            page = self.paginate_queryset(queryset)
            serializer=FlightSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            errs = {'errors': [{
                'status': 400,
                'detail': str(e),
                'source': {'pointer': request.path}
            }]}
            error_logger.error({'response': errs})
            return Response(errs, status.HTTP_400_BAD_REQUEST)