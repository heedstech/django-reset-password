import pytest

from django.urls import reverse

from rest_framework.test import APIClient
from password_reset.models import RecoveryCode


@pytest.fixture
def api():
    return APIClient()


@pytest.mark.django_db
def test_response_is_empty(api, user):
    response = api.post(reverse('reset-password'),
                        {'email': user.email})
    assert response.status_code == 204
    assert response.data is None


@pytest.mark.django_db
def test_new_code_generated_and_email_is_sent(api, user, mailoutbox):
    api.post(reverse('reset-password'), {'email': user.email})
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == 'E-mail de recuperação de senha'


@pytest.mark.django_db
def test_email_does_not_exist(api, mailoutbox):
    response = api.post(reverse('reset-password'),
                        {'email': 'no@exists.email'})
    assert len(mailoutbox) == 0
    assert response.status_code == 204
    assert response.data is None


@pytest.mark.django_db
def test_recovery_code_is_created(api, user):
    response = api.post(reverse('reset-password'),
                        {'email': user.email})
    recovery_code = RecoveryCode.objects.first()
    assert recovery_code.user == user
