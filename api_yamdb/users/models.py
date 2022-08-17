from django.contrib.auth.models import AbstractUser
from django.db import models

from core.validators import UserRegexValidator, validate_username

USER: str = 'user'
MODERATOR: str = 'moderator'
ADMIN: str = 'admin'


class User(AbstractUser):
    """
    Пользовательская модель User.
    Добавлены роли и пользовательские поля.
    Переопределены стандартные поля.
    Добавлены пользовательские методы.
    """
    ROLE_CHOICES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        validators=[validate_username, UserRegexValidator]
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        'email',
        blank=False,
        unique=True,
    )
    role = models.CharField(
        'Права пользователя',
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
        blank=False,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    is_activate = models.BooleanField(
        'Получение токена',
        default=False,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self) -> bool:
        return self.role == ADMIN or self.is_staff

    @property
    def is_moderator(self) -> bool:
        return self.role == MODERATOR

    def __str__(self) -> str:
        return self.username
