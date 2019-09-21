from django.contrib.auth import get_user_model,authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework import status
from base.serializers import ErrorHandlerSerializerMixin
from users.models import User



class SignupSerializer(serializers.ModelSerializer,ErrorHandlerSerializerMixin):
    class Meta:
        model = User
        fields = ['username',
                  'password',
                  're_password',
                  'address',
                  'mobile_number',
                  'first_name',
                  'last_name',
                  'birth_date',
                  'birth_place',
                  'email']

    # password = serializers.CharField()
    email = serializers.CharField()
    username = serializers.CharField(max_length=32, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)
    re_password = serializers.CharField(min_length=8, write_only=True)
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        if password==re_password :
                UserModel = get_user_model()
                if UserModel.objects.filter(username=username).count():
                    raise ValidationError('This user already exist.')
        else:
            raise ValidationError('Tha password and re_password are not same.')
        return attrs


class LoginPassSerializer(serializers.Serializer,ErrorHandlerSerializerMixin):
    username = serializers.CharField()
    password=serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        UserModel = get_user_model()
        assert UserModel.objects.filter(username=username,enabled=True).count() == 1, \
            ValidationError('This user does not exist')
        user = UserModel.objects.get(username=username,enabled=True)
        assert user.is_active, ValidationError('This user is inactive')
        assert user.check_password(password),ValidationError('password is wrong')
        return user
