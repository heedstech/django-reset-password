import pytest


def pytest_configure():
    from django.conf import settings

    MIDDLEWARE = (
        "django.middleware.common.CommonMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    )

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"},
            "other": {"ENGINE": "django.db.backends.sqlite3", "NAME": "other"},
        },
        SITE_ID=1,
        SECRET_KEY="not very secret in tests",
        USE_I18N=True,
        STATIC_URL="/static/",
        ROOT_URLCONF="password_reset.urls",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
            },
        ],
        MIDDLEWARE=MIDDLEWARE,
        MIDDLEWARE_CLASSES=MIDDLEWARE,
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.staticfiles",
            "rest_framework",
            "tests",
            'password_reset',
        ),
        PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
        SIMPLE_JWT={
            "BLACKLIST_AFTER_ROTATION": True,
        },
    )

    try:
        # import os
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.test_settings")

        import django
        django.setup()

    except AttributeError:
        pass


@pytest.fixture
def user(django_user_model):
    email = "user@email.com"
    password = "bar"
    return django_user_model.objects.create_user(
        username='test',
        email=email,
        password=password,
        is_active=True,
    )
