from django.conf.urls import url
from authentication.views import (SignupView,
                            LoginByPasswordView,
                            )

urlpatterns = [
    url(r'^signup/$', SignupView.as_view()),
    url(r'^login/$', LoginByPasswordView.as_view()),
]
