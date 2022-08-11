from django.contrib.auth.models import AbstractUser
from django.db import models

from settings import ADMIN, MODERATOR, USER


class User(AbstractUser):
    """Расширенная модель User.
    Добавлены роли и пользовательские поля.
    Переопределены стандартные поля.
    """

    ROLE_CHOICES = (
        (ADMIN, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (USER, 'Администратор'),
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
        default=ADMIN,
        blank=False,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    def __str__(self) -> str:
        return self.username
