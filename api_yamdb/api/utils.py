from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from settings import FROM_EMAIL


def get_tokens_for_user(user):
    """Генерация токена."""
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token),
    }


def new_user_get_confirmation_code_and_email(user):
    """Получение проверочного кода и email."""
    url_point = '.../api/v1/auth/token/'  # как чисто достать URL
    confirmation_code = default_token_generator.make_token(user)
    try:
        send_mail(
            'Получение токена на проекте YaMDB',
            f'{user}, '
            f'для получения токена пройдите по ссылке {url_point}. '
            f'и введите проверочный код: {confirmation_code}.',
            FROM_EMAIL,
            [user.get_email()],
        )
    except BadHeaderError:
        return Response({
            'message': 'Письмо с кодом проверки не может быть '
                       'отправлено. Обратитесь в тех.поддержку.'
        }, status=status.HTTP_400_BAD_REQUEST)
