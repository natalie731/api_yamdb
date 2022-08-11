from webbrowser import get
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, verbose_name='Слаг жанра')

    class Meta:
        ordering = ['-id']
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='Слаг категории')

    class Meta:
        ordering = ['-id']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        max_length=256,
        verbose_name='Навзвание произведения'
    )
    year = models.SmallIntegerField(verbose_name='Год создания произведения')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    description = models.TextField('Описание')
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')

    class Meta:
        ordering = ['-id']
        verbose_name = "Произведние"
        verbose_name_plural = "Произведния"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Отзыв к произведению'
    )

    text = models.TextField(
        help_text='Введите текст отзыва',
        verbose_name='Текст отзыва'
    )

    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    score = models.FloatField(
        validators=[MinValueValidator(0.0),
                    MaxValueValidator(10.0)],
        verbose_name='Рейтинг'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'


class Comment(models.Model):
    reviews = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Текст комментария'
    )
    text = models.TextField(
        help_text='Введите текст комментария',
        verbose_name='Текст комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
