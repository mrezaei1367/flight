from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import BasePagination


class BaseModelViewset(ModelViewSet, NestedViewSetMixin):
    pagination_class = BasePagination
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ('created_date', 'update_time')

    def get_queryset(self):
        return self.queryset.filter(soft_deleted=False)

    def create(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'id': serializer.data['id']}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        self.instance = serializer.save()

    def destroy(self, request, *args, **kwargs):
        class DynamicDeleteSerializer(ModelSerializer):
            class Meta:
                model = self.get_serializer_class().Meta.model
                fields = []

            def validate(self, attrs):
                if self.instance.soft_deleted:
                    raise ValidationError('The selected object does not exist or already deleted.')
                return attrs

        try:
            instance = self.get_object()
            serializer = DynamicDeleteSerializer(instance, request.data)
            serializer.is_valid(raise_exception=True)
            instance.soft_deleted = True
            instance.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            if type(e) is ValidationError:
                raise e

        return Response({
            "errors": [
                {
                    "status": 1,
                    "key": "non_field_errors",
                    "detail": "The selected object does not exist or already deleted."
                }
            ]
        }, status=status.HTTP_205_RESET_CONTENT)
