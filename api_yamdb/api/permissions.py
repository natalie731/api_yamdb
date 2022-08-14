from rest_framework import permissions


class AdminOrSuperUserOnly(permissions.BasePermission):
    """Разрешения только для администраторов."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin()
                     or request.user.is_superuser))


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.role == 'admin' or request.user.is_superuser))
                )


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin()
                or request.user.is_moderator())

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
