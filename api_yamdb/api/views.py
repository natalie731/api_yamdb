from rest_framework import filters, mixins, viewsets
from users.models import User
from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleListSerializer, TitleCreateSerializer, UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
    #permission_classes = [IsAuthenticatedOrReadOnly, Админ или только чтение]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'update',):
            return TitleCreateSerializer
        return TitleListSerializer


class CategoryViewSet(viewsets.CreateListDestroyViewSet):
    """
    Возвращает список, создает новые и удаляет существующие категории
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    #permission_classes = [Админ или только чтение]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(viewsets.CreateListDestroyViewSet):
    """
    Возвращает список, создает новые и удаляет существующие жанры
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    #permission_classes = [Админ или только чтение]
    search_fields = ['name']
    lookup_field = 'slug'
