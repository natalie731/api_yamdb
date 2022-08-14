from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы можете добавить только один'
                                      ' отзыв к произведению')
        return data

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
        read_only_fields = ("reviews",)


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователей.
    """

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role',)

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError(
                'Измените имя пользователя.'
            )
        return data


class AuthSerializer(UserSerializer):
    """
    Сериализатор расширенный для аутентификации.
    """
    email = serializers.EmailField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'email',)


class TokenSerializer(serializers.Serializer):
    """
    Сериализатор для выдачи токенов.
    """
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий
    """

    class Meta:
        fields = ('name', 'slug',)
        model = Category
        lookup_field = 'slug'


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
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))
        return rating.get('score__avg')
