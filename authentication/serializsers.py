from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',
                  'password',
                  're_password',
                  'address',
                  'mobile_number',
                  'first_name',
                  'last_name',
                  'birth_date',
                  'birth_place']

    password = serializers.CharField()
    re_password = serializers.CharField()
    email = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        if password==re_password :
                UserModel = get_user_model()
                if UserModel.objects.filter(username=email).count():
                    raise ValidationError('This user already exist.')
        else:
            raise ValidationError('Tha password and re_password are not same.')
        return attrs

# class VerifySerializer(serializers.ModelSerializer, ErrorHandlerSerializerMixin):
#     class Meta:
#         model = User
#         fields = ['email',
#                   'verify_code']
#
#     verify_code = serializers.CharField(max_length=40)
#     email = serializers.EmailField(max_length=255)
#     def _expire(self, verify_request):
#         verify_request.soft_deleted = True
#         verify_request.save()
#
#     def validate(self, attrs):
#         verify_code = attrs.get('verify_code')
#         email = attrs.get('email')
#         # self.verify_type = attrs.get('verify_type')
#         verify_request=VerifyRequest.objects.filter(email=email,soft_deleted=False).first()
#
#         if verify_request  or verify_code==GOD_SMS_CODE :
#             if verify_request.verification_code == verify_code or verify_code==GOD_SMS_CODE:
#                 # if (verify_request.created_date + timedelta(seconds=COUNTER_SECONDS)) < timezone.now():
#                 #     self._expire(verify_request)
#                 #     raise ValidationError("Verification code is invalid")
#                 self._expire(verify_request)
#             else:
#                 verify_request.counter_tries += 1
#                 verify_request.soft_deleted = verify_request.counter_tries >= COUNTER_TRIES
#                 verify_request.save()
#                 raise ValidationError('کد تایید معتبر نیست.')
#         else:
#             raise ValidationError('کد تایید معتبر نیست.')
#         return attrs


class LoginPassSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password=serializers.CharField()
    user_type = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user_type = attrs.get('user_type')
        UserModel = get_user_model()
        assert UserModel.objects.filter(username=email,enabled=True).count() == 1, \
            ValidationError('This user does not exist')
        user = UserModel.objects.get(username=email,enabled=True)
        assert user.is_active, ValidationError('This user is inactive')
        assert user.check_password(password),ValidationError('password is wrong')
        return user


class ForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

    email = serializers.EmailField(max_length=255)

    def validate(self,attrs):
        email=attrs.get('email')
        UserModel = get_user_model()
        assert UserModel.objects.filter(username=email, enabled=True).count() == 1, \
            ValidationError('This user does not exist')
        user = UserModel.objects.get(username=email, enabled=True)
        return user
