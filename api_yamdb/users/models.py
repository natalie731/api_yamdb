from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 1
    MODERATOR = 2
    ADMIN =3

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
