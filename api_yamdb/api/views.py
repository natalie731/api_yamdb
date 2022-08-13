from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Review
from .permissions import AdminOrSuperUserOnly, IsAuthorModeratorAdminOrReadOnly
from .serializers import (AuthSerializer, CategorySerializer, GenreSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          TokenSerializer, UserSerializer, ReviewSerializer,
                          CommentSerializer)
from .utils import (get_tokens_for_user,
                    new_user_get_confirmation_code_and_email)

User = get_user_model()


class AuthViewSet(APIView):
    """
    Регистрация пользователя.
    """
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_active=False)
            user = User.objects.get(
                username=serializer.validated_data['username']
            )
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
    lookup_field = 'username'

    def perform_create(self, serializer):
        """Переопределяем создание пользователя. Выдаем токен.
        """
        serializer.save()
        user = User.objects.get(username=serializer.validated_data['username'])
        get_tokens_for_user(user)

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        """Добавляем пользовательскую страницу,
        которую не генерирует роутер.
        """
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(user,
                                             data=request.data,
                                             partial=True)
            if serializer.is_valid():
                serializer.save(role=user.role)
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


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


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Возвращает список, создает / редактирует / удаляет отзывы
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Возвращает список, создает / редактирует / удаляет комментарии
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
