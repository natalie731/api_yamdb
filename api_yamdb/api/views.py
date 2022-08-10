from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.db import DatabaseError, transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .serializers import TokenSerializer, UserSerializer

FROM_EMAIL = 'from@example.com'


def get_tokens_for_user(user):
    """Выдает токен."""
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }


class UserViewSet(APIView):
    """Создание пользователя.
    Контроль отправки сообщений.
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        url_point = request.build_absolute_uri('/api/v1/auth/token/')
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
            except DatabaseError:
                return Response({
                    'message': 'Что-то пошло не так, повторите регистрацию.'
                }, status=status.HTTP_400_BAD_REQUEST)

            confirmation_code = (
                default_token_generator._make_token_with_timestamp(
                    User.objects.get(
                        username=serializer.validated_data['username']
                    ),
                    3 * 24 * 60 * 60
                )
            )
            try:
                send_mail(
                    'Получение токена на проекте YaMDB',
                    f'{serializer.validated_data["username"]}, '
                    f'для получения токена пройдите по ссылке {url_point}. '
                    f'и введите временный пароль: {confirmation_code}. '
                    'Срок действия пароля 3 дня.',
                    FROM_EMAIL,
                    [serializer.validated_data['email']],
                )
            except BadHeaderError:
                return Response({
                    'message': 'Письмо с кодом проверки не может быть '
                               'отправлено. Обратитесь в тех.поддержку.'
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    """Валидация пользователя перед получением токена."""

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            valid_username = serializer.validated_data['username']
            valid_code = serializer.validated_data['confirmation_code']
            if User.objects.filter(username=valid_username).exists():
                user = User.objects.get(username=valid_username)

                if default_token_generator.check_token(
                    user=user,
                    token=valid_code
                ):

                    if user.is_active:
                        return Response({
                            'message': 'Токен уже выдан.'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    return Response(get_tokens_for_user(user),
                                    status=status.HTTP_200_OK)

                return Response({
                    'message': 'Проверочный код не действителен.'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'message': 'Пользователь не найден.'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
