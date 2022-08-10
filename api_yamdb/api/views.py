from rest_framework import mixins, viewsets

from users.models import User
from .serializers import UserSerializer


class CreateUserViewSet(mixins.CreateModelMixin):
    pass


class UserViewSet(CreateUserViewSet, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        #try:
        #    confirmation_code = encode('')
        #except Exception('')
        serializer.save()
        #try:
        #    send_mail(
        #        'Подтверждение регистрации на проекте YaMDB',
        #        f'Пройдите по ссылке http/api/v1/auth/token
        #          Введите этот код проверки {confirmation_code}',
        #        'from@example.com',
        #        ['to@example.com'],
        #        fail_silently=False, # Сообщать об ошибках («молчать ли об ошибках?»)
        #    )
        #except Exception('')


