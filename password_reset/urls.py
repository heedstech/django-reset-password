from django.urls import path

from password_reset.views import reset_password


urlpatterns = [
    path('reset/', reset_password, name='reset-password'),
]
