from rest_framework import permissions


class AdminOrSuperUserOnly(permissions.BasePermission):
    """Разрешения только для администраторов."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin()
                    or request.user.is_superuser)
        return False
