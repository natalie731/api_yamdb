from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username',
                    'email', 'first_name',
                    'last_name', 'role', 'bio',
                    'is_active', 'date_joined')
    readonly_fields = ('confirmation_code',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'

admin.site.register(User, UserAdmin)
