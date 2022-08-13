from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username',
                    'email', 'first_name',
                    'last_name', 'role', 'bio',
                    'is_active', 'date_joined')
    search_fields = ('username',)
    empty_value_display = '-пусто-'
    exclude = ('is_staff', 'groups',
               'user_permissions', 'last_login')
    readonly_fields = ('date_joined', 'is_active',)


admin.site.register(User, UserAdmin)
