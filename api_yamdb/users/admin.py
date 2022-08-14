from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'role',
                    'email', 'first_name',
                    'last_name', 'date_joined',
                    'is_activate')
    search_fields = ('username',)
    empty_value_display = '-пусто-'
    exclude = ('is_staff', 'groups', 'is_active',
               'user_permissions', 'last_login')
    readonly_fields = ('date_joined', 'is_activate',)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
