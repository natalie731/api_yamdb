from django.contrib.auth import get_user_model
from django.core.mail import BadHeaderError, send_mail
from django.db import DatabaseError, transaction
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import AdminOrSuperUserOnly
from reviews.models import Category, Genre, Title
from settings import FROM_EMAIL
from .serializers import (AuthSerializer, CategorySerializer, GenreSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          TokenSerializer, UserSerializer)

User = get_user_model()


def get_tokens_for_user(user):
    """Генерация токена."""
    refresh = RefreshToken.for_user(user)
    return {
        'token': str(refresh.access_token),
    }


class AuthViewSet(APIView):
    """
    Регистрация пользователя.
    """
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        url_point = request.build_absolute_uri('/api/v1/auth/token/')
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save(is_active=False)
            except DatabaseError:
                return Response({
                    'message': 'Что-то пошло не так, повторите регистрацию.'
                }, status=status.HTTP_400_BAD_REQUEST)
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            user = User.objects.get(username=username)

            try:
                send_mail(
                    'Получение токена на проекте YaMDB',
                    f'{serializer.validated_data["username"]}, '
                    f'для получения токена пройдите по ссылке {url_point}. '
                    f'и введите проверочный код: {user.confirmation_code}. '
                    'Срок действия кода 1 день.',
                    FROM_EMAIL,
                    [email],
                )
            except BadHeaderError:
                return Response({
                    'message': 'Письмо с кодом проверки не может быть '
                               'отправлено. Обратитесь в тех.поддержку.'
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenViewSet(APIView):
    """
    Получение токена.
    """
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            valid_username = serializer.validated_data['username']
            valid_code = serializer.validated_data['confirmation_code']
            if User.objects.filter(username=valid_username).exists():
                user = User.objects.get(username=valid_username)

                if user.get_confirmation_code() == valid_code:
                    User.objects.filter(username=user).update(is_active=True)
                    return Response(get_tokens_for_user(user),
                                    status=status.HTTP_200_OK)

                return Response({
                    'message': 'Проверочный код не действителен.'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'message': 'Пользователь не найден.'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Предоставляет CRUD-действия для пользователей.
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = (AdminOrSuperUserOnly,)
    pagination_class = PageNumberPagination
    search_fields = ('username',)

    # def perform_create(self, request):
    #     pass


class TitlesViewSet(viewsets.ModelViewSet):
    """
    Предоставляет CRUD-действия для произведений
    """
    queryset = Title.objects.all()
    filter_backends = (filters.SearchFilter,)
    filterset_fields = (
        'category',
        'genre',
        'name',
        'year',
    )
    # permission_classes = [IsAuthenticatedOrReadOnly, Админ или только чтение]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'update',):
            return TitleCreateSerializer
        return TitleListSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Возвращает список, создает новые и удаляет существующие категории
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    # permission_classes = [Админ или только чтение]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    """
    Возвращает список, создает новые и удаляет существующие жанры
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    # permission_classes = [Админ или только чтение]
    search_fields = ['name']
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    pass
