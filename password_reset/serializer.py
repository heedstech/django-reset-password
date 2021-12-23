from rest_framework import serializers

from django.contrib.auth import get_user_model

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
