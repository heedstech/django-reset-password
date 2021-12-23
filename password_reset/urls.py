from django.urls import path

from .views import reset_password


urlpatterns = [
    path('reset/', reset_password, name='reset-password'),
]
