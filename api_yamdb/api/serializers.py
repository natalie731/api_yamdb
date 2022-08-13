from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    review = SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class AuthSerializer(serializers.ModelSerializer):
    """
    Сериализатор для аутентификации пользователя.
    """

    class Meta:
        fields = ('username', 'email',)
        model = User

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError(
                'Измените имя пользователя.'
            )
        return data


class TokenSerializer(serializers.Serializer):
    """
    Сериализатор для выдачи токенов.
    """
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(AuthSerializer):
    """
    Сериализатор расширенный для пользователя.
    """

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role',)


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий
    """

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров
    """

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания произведений
    """
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = ('__all__')
        model = Title


class TitleListSerializer(serializers.ModelSerializer):
    """
    Сериализатор вывода списка произведений
    """
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    # rating

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')
        model = Title
