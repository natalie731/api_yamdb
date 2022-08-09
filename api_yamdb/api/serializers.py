import email
from typing_extensions import Required
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email',)
        model = User
