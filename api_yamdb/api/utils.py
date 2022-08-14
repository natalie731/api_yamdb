from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

URL_POINT: str = settings.ALLOWED_HOSTS[0] + '/api/v1/auth/token/'
FROM_EMAIL: str = 'from@example.com'
SUBJECT: str = 'Получение токена на проекте YaMDB.'
MESSAGE: str = ('{}, для получения токена '
                f'пройдите по ссылке {URL_POINT} и введите '
                'проверочный код: {}')
# FROM_EMAIL: str = 'info@yambl.ru'


def get_tokens_for_user(user):
    """Генерация токена."""
    access = AccessToken.for_user(user)
    return {'token': str(access), }


def new_user_get_email(user, confirmation_code):
    """Отправляем email пользователю."""
    try:
        send_mail(
            SUBJECT,
            MESSAGE.format(user, confirmation_code),
            FROM_EMAIL,
            [user.email],
        )
    except BadHeaderError:
        return Response({
            'message': 'Письмо с кодом проверки не может быть '
                       'отправлено. Обратитесь в тех.поддержку.'
        }, status=status.HTTP_400_BAD_REQUEST)
