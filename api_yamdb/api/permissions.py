from rest_framework import permissions


class AdminOrSuperUserOnly(permissions.BasePermission):
    """Разрешения только для администраторов."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin()
                    or request.user.is_superuser)
        return False


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        return (
                obj.author == request.user
                or request.user.is_admin()
                or request.user.is_moderator()
                or request.method in permissions.SAFE_METHODS
        )
