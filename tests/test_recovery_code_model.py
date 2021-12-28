import pytest

from django.urls import reverse
from django.db import IntegrityError

from rest_framework.test import APIClient

from password_reset.models import RecoveryCode
from password_reset.utils.code_generator import generate_code, generate_hash


@pytest.mark.django_db
def test_unique_active_hash_code_fail_with_duplicated_code(user):
    code = generate_code(user)
    hash_code = generate_hash(code, user)
    with pytest.raises(IntegrityError):
        RecoveryCode(user=user, hash_code=hash_code).save()


@pytest.mark.django_db
def test_pass_when_duplicated_code_is_inactive(user):
    code = generate_code(user)
    hash_code = generate_hash(code, user)
    recovery_code = RecoveryCode.objects.first()
    recovery_code.is_active = False
    recovery_code.save()
    RecoveryCode(user=user, hash_code=hash_code).save()
    assert RecoveryCode.objects.filter(hash_code=hash_code).count() == 2
