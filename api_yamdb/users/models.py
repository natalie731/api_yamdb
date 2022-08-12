from django.contrib.auth.models import AbstractUser
from django.db import models

from settings import ADMIN, MODERATOR, USER


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

    def get_email(self) -> str:
        return self.email

    def is_admin(self) -> bool:
        return self.role == ADMIN

    def is_moderator(self) -> bool:
        return self.role == MODERATOR

    def __str__(self) -> str:
        return self.username
