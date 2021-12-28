from django.urls import path

from .views import reset_password, reset_password_confirm


urlpatterns = [
    path('reset/', reset_password, name='reset-password'),
    path('reset-confirm/', reset_password_confirm, name='reset-password-confirm'),
]
