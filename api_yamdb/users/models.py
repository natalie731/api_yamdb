from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
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
    role = models.PositiveSmallIntegerField(
        'Права пользователя',
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='Unique_user')]
