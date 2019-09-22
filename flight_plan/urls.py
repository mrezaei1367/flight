from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet


router = DefaultRouter()
router.register(r'', FlightViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    ]