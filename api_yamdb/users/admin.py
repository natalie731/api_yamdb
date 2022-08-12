from django.contrib import admin

from api.utils import get_tokens_for_user
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username',
                    'email', 'first_name',
                    'last_name', 'role', 'bio',
                    'is_active', 'date_joined')
    search_fields = ('username',)
    empty_value_display = '-пусто-'

    def save_model(self, request, obj, form, change):
        """
        Переопределен метод создания пользователя через админку.
        Добавлена выдача токена.
        """
        obj.save()
        get_tokens_for_user(obj)


admin.site.register(User, UserAdmin)
