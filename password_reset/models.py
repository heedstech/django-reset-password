from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from datetime import timedelta

User = get_user_model()


class RecoveryCode(models.Model):
    hash_code = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expire_at = models.DateTimeField(default=lambda: timezone.now() + timedelta(minutes=5))
