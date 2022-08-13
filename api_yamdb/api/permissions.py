from rest_framework import permissions


class AdminOrSuperUserOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin()
                    or request.user.is_superuser)

    # def has_object_permission(self, request, view, obj):
    #     return request.user.is_admin


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.role == 'admin' or request.user.is_superuser))
                )
