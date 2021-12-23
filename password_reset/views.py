from rest_framework.decorators import api_view

from rest_framework import status
from rest_framework.response import Response

from password_reset.utils.code_generator import generate_code
from password_reset.utils.email import PasswordResetEmail
from password_reset.serializer import SendEmailResetSerializer


@api_view(['POST'])
def reset_password(request):
    serializer = SendEmailResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.get_user()


    if user:
        code = generate_code(user)
        context = {"code": code}
        to = [user.email]
        PasswordResetEmail(request, context).send(to)

    return Response(status=status.HTTP_204_NO_CONTENT)
