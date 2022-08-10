from sqlite3 import register_adapter
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель User. Добавлены роли и пользовательские поля.
    Переопределены стандартные поля.
    """
    USER = 1
    MODERATOR = 2
    ADMIN = 3

    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
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
    role = models.PositiveSmallIntegerField(
        'Права пользователя',
        choices=ROLE_CHOICES,
        default=USER,
        blank=False,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    is_active = models.BooleanField(default=False)
    register_date = models.DateTimeField(auto_now_add=True)
