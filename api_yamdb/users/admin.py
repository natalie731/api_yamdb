from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username',
                    'email', 'first_name',
                    'last_name', 'role', 'bio',
                    'is_activate', 'date_joined')
    search_fields = ('username',)
    empty_value_display = '-пусто-'
    exclude = ('is_staff', 'groups', 'is_active',
               'user_permissions', 'last_login')
    readonly_fields = ('date_joined', 'is_activate',)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
