from django.core.mail import BadHeaderError, send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from uuid import uuid4

from .serializers import UserSerializer

FROM_EMAIL = 'from@example.com'


class UserViewSet(APIView):
    """Контролируем отправку сообщений пользователю и рандомный код в базу."""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        url_point = request.build_absolute_uri('/api/v1/auth/token/')
        confirmation_code = uuid4()
        if serializer.is_valid():
            try:
                send_mail(
                    'Получение токена на проекте YaMDB',
                    f'Для получения токена пройдите по ссылке {url_point}.'
                    f' и введите код проверки - {confirmation_code}',
                    FROM_EMAIL,
                    [serializer.validated_data['email']],
                )
            except BadHeaderError:
                return Response({
                    'message': 'Что-то пошло не так, повторите регистрацию.'
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(confirmation_code=confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
