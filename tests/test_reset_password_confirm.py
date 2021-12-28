import pytest

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from datetime import timedelta

from password_reset.models import RecoveryCode
from password_reset.utils.code_generator import generate_code


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def recovery_code(user):

    def _wrapper(expired=False):
        code = generate_code(user)
        recovery_code = RecoveryCode.objects.first()
        if expired:
            recovery_code.expire_at = timezone.now() - timedelta(minutes=5)
        recovery_code.save()
        return (code, recovery_code)

    return _wrapper

@pytest.fixture
def data(user):

    def _wrapper(code, password_match=True):
        return {
            "code": code,
            "password": "password",
            "password2": "password" if password_match else "password2",
            "email": user.email
        }

    return _wrapper


@pytest.mark.wip
@pytest.mark.django_db
def test_response_is_empty(api, recovery_code, data):
    code, recovery_code = recovery_code()

    response = api.post(reverse('reset-password-confirm'),
                        data(code))
    assert response.status_code == 204
    assert response.data is None


@pytest.mark.django_db
def test_fail_with_not_found_code(api, data):
    data = data('000000')
    response = api.post(reverse('reset-password-confirm'),
                        data)
    assert response.status_code == 400
    data = response.json()
    assert data == {'code': ['Code not found.']}


@pytest.mark.django_db
def test_fail_if_does_not_required_field(api, recovery_code):
    response = api.post(reverse('reset-password-confirm'))
    assert response.status_code == 400
    data = response.json()
    assert data == {
        'code': ['This field is required.'],
        'password': ['This field is required.'],
        'password2': ['This field is required.'],
        'email': ['This field is required.']
    }


@pytest.mark.django_db
def test_fail_if_code_has_invalid_length(api, data):
    data = data('000')
    response = api.post(reverse('reset-password-confirm'),
                        data)
    assert response.status_code == 400
    data = response.json()
    assert data == {'code': ['Code must be 6 character long.']}


@pytest.mark.django_db
def test_fail_if_recovery_code_is_expired(api, recovery_code, data):
    code, recovery_code = recovery_code(expired=True)
    response = api.post(reverse('reset-password-confirm'),
                        data(code))
    assert response.status_code == 400
    data = response.json()
    assert data == {'code': ['Code is expired.']}


@pytest.mark.django_db
def test_inactivate_recovery_code_after_successful_reset(api, recovery_code, data):
    code, recovery_code = recovery_code()
    response = api.post(reverse('reset-password-confirm'),
                        data(code))
    recovery_code = RecoveryCode.objects.first()
    assert recovery_code.is_active == False


@pytest.mark.django_db
def test_email_was_sent(api, recovery_code, mailoutbox, data):
    code, recovery_code = recovery_code()
    response = api.post(reverse('reset-password-confirm'),
                        data(code))
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == 'Senha Alterada'


@pytest.mark.django_db
def test_password_not_match(api, recovery_code, data):
    code, recovery_code = recovery_code()
    response = api.post(reverse('reset-password-confirm'),
                        data(code, password_match=False))
    assert response.status_code == 400
    data = response.json()
    assert data == {'password': ['Passwords must match.']}


@pytest.mark.django_db
def test_password_was_changed(api, recovery_code, data, user):
    code, recovery_code = recovery_code()
    response = api.post(reverse('reset-password-confirm'),
                        data(code))
    User = get_user_model()
    user_after = User.objects.get(email=user.email)
    assert user_after.password != user.password


@pytest.mark.django_db
def test_fail_if_email_not_found(api, recovery_code, data):
    code, recovery_code = recovery_code()
    data = data(code)
    data['email'] = 'some@email.com'
    response = api.post(reverse('reset-password-confirm'),
                        data)
    assert response.status_code == 400
    data = response.json()
    assert data == {'code': ['User was not found for this code.']}
