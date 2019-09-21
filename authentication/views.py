from django.conf import settings
from django.contrib.auth import login, get_user_model, authenticate
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from .utils import import_callable
from .settings import TOKEN_CREATOR,TOKEN_SERIALIZER
from .serializsers import SignupSerializer,LoginPassSerializer
from .models import TokenByIPPayload
from users.models import User


create_token = import_callable(TOKEN_CREATOR)


class SignupView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
    token_model = TokenByIPPayload
    throttle_classes = (AnonRateThrottle,)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request, *args, **kwargs):
        self.serializer = SignupSerializer(data=request.data)
        try:
            UserModel=get_user_model()
            self.serializer.is_valid(raise_exception=True)
            usr=UserModel.objects.create(
                username=self.serializer.validated_data['username'],
                password=self.serializer.validated_data['password'],
                address=self.serializer.validated_data['address'],
                first_name=self.serializer.validated_data['first_name'],
                last_name=self.serializer.validated_data['last_name'],
                mobile_number=self.serializer.validated_data['mobile_number'],
                enabled=True,
                email=self.serializer.validated_data['email']
            )
            # usr.set_password(self.serializer.validated_data['password'])
            # user=UserModel.objects.get(username=usr.username)
            token = create_token(self.token_model, usr, request)
            authenticate(username=self.serializer.validated_data['username'], token_key=token.key)
            return Response({'message': 'Successfully',
                             'token': token.key,
                             'id': usr.id,
                             'username': usr.username,
                             'status': 200
                             },
                            status.HTTP_200_OK)

        except Exception as e:
            if settings.DEBUG:
                raise e
            errs = {'errors':
                        {'status': 400,
                         'detail': 'Not Acceptable',
                         'source': {'pointer': request.path}
                         }}
            return Response(errs, status.HTTP_400_BAD_REQUEST)


class LoginByPasswordView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginPassSerializer
    token_model = TokenByIPPayload
    response_serializer = TOKEN_SERIALIZER
    throttle_classes = (AnonRateThrottle,)

    def login(self):
        self.user = self.serializer.validated_data
        if self.user.auth_token:
            self.token=self.user.auth_token
        else:
            self.token = create_token(self.token_model, self.user, self.serializer.context['request'])
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, self.user)

    def get_response(self):
        return Response(
            {'token':str(self.token.key)},
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()