from django.contrib.auth import get_user_model
from django.db import models

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
