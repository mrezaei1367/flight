from six import string_types
from ipware.ip import get_ip
from importlib import import_module
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from rest_framework.authtoken.models import Token as DefaultTokenModel


def import_callable(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, string_types)
        package, attr = path_or_callable.rsplit('.', 1)
        return getattr(import_module(package), attr)
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
TokenModel = import_callable(getattr(settings, 'REST_AUTH_TOKEN_MODEL', DefaultTokenModel))


def default_create_token(token_model, user):
    token, _ = token_model.objects.get_or_create(user=user)
    return token


def jwt_token_creator(token_model, user, request):
    payload = jwt_payload_handler(user)
    payload["ip"] = get_ip(request)
    token_value = jwt_encode_handler(payload)
    token = token_model.objects.create(user=user, key=token_value)
    return token
