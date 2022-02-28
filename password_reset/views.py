from rest_framework.decorators import api_view

from rest_framework import status
from rest_framework.response import Response

from .utils.code_generator import generate_code
from .utils.email import PasswordResetEmail, PasswordChangedConfirmationEmail
from .serializers import SendEmailResetSerializer, SendCodeResetSerializer
from .models import RecoveryCode


@api_view(['POST'])
def reset_password(request):
    serializer = SendEmailResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.get_user()


    if user:
        code = generate_code(user)
        context = {
            "code": code,
            "email": user.email
        }
        to = [user.email]
        PasswordResetEmail(request, context).send(to)

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def reset_password_confirm(request):
    serializer = SendCodeResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    hash_code = serializer.data['code']
    password = serializer.data['password']
    recovery_code = RecoveryCode.objects.get(hash_code=hash_code, is_active=True)
    recovery_code.is_active = False
    recovery_code.save()
    recovery_code.user.set_password(password)
    recovery_code.user.save()
    to = [recovery_code.user.email]
    PasswordChangedConfirmationEmail(request).send(to)
    return Response(status=status.HTTP_204_NO_CONTENT)
