from django.conf.urls import url,include
from .views import UserProfileView



urlpatterns = [
    url(r'^profile/$', UserProfileView.as_view()),


]
