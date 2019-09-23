
def search_flight(queryset, flight_name, departure, destination, scheduled_date):
    if flight_name:
        queryset = queryset.filter(flight_name__icontains=flight_name)
    if departure:
        queryset = queryset.filter(departure__icontains=departure)
    if destination:
        queryset = queryset.filter(destination__icontains=destination)
    if scheduled_date:
        queryset = queryset.filter(scheduled_date__date=scheduled_date)
    queryset = queryset.order_by('scheduled_date')
    return queryset
