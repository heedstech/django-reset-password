from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import RecoveryCode
from .utils.code_generator import generate_hash

User = get_user_model()


class UserFunctionsMixin:
    def get_user(self, is_active=True):
        try:
            return User._default_manager.get(
                is_active=is_active,
                email=self.data.get("email", ""),
            )
        except User.DoesNotExist:
            pass


class SendEmailResetSerializer(serializers.Serializer, UserFunctionsMixin):
    email = serializers.EmailField()


class SendCodeResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)


    def validate_password(self, password):
        data = self.get_initial()
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords must match.')
        return password

    def validate_code(self, code):
        data = self.get_initial()

        if (len(code) != 6):
            raise serializers.ValidationError('Code must be 6 character long.')

        try:
            user = User._default_manager.get(
                is_active=True,
                email=data.get("email", ""),
            )
        except User.DoesNotExist:
            raise serializers.ValidationError('User was not found for this code.')

        hash_code = generate_hash(code, user)
        try:
            recovery_code = RecoveryCode.objects.get(hash_code=hash_code, is_active=True)
            if timezone.now() > recovery_code.expire_at:
                raise serializers.ValidationError('Code is expired.')
            return hash_code
        except RecoveryCode.DoesNotExist:
            raise serializers.ValidationError('Code not found.')
