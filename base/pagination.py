from rest_framework.pagination import LimitOffsetPagination


class BasePagination(LimitOffsetPagination):
    max_limit = 20
    default_limit = 10
