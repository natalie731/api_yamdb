from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Category, Genre, Title
from .filters import TitlesFilter
from .permissions import AdminOrSuperUserOnly, AdminOrReadOnly
from .serializers import (AuthSerializer, CategorySerializer, GenreSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          TokenSerializer, UserSerializer)
from .utils import get_tokens_for_user, new_user_get_confirmation_code_and_email

User = get_user_model()


class AuthViewSet(APIView):
    """
    Регистрация пользователя.
    """
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_active=False)
            user = User.objects.get(username=serializer.validated_data['username'])
            new_user_get_confirmation_code_and_email(user)
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

                if default_token_generator.check_token(
                    user=user,
                    token=valid_code
                ):
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

    def perform_create(self, serializer):
        serializer.save()
        user = User.objects.get(username=serializer.validated_data['username'])
        get_tokens_for_user(user)


class TitlesViewSet(viewsets.ModelViewSet):
    """
    Предоставляет CRUD-действия для произведений
    """
    queryset = Title.objects.all()
    serializer_class = TitleListSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleListSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Возвращает список, создает новые и удаляет существующие категории
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    @action(detail=False,
            methods=['delete'],
            url_path=r'(?P<slug>[-\w]+)',
            permission_classes=(AdminOrSuperUserOnly,)
            )
    def slug(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    """
    Возвращает список, создает новые и удаляет существующие жанры
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    @action(detail=False,
            methods=['delete'],
            url_path=r'(?P<slug>[-\w]+)',
            permission_classes=(AdminOrSuperUserOnly,)
            )
    def slug(self, request, slug):
        genre = get_object_or_404(Genre, slug=slug)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CommentViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    pass
