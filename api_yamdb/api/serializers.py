from rest_framework import serializers

from users.models import User


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email',)
        model = User

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError(
                'Измените имя пользователя.'
            )
        return data


class TokenSerializer(serializers.Serializer):

    username = serializers.CharField()
    confirmation_code = serializers.CharField()
