from rest_framework import permissions


class AdminOrSuperUserOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin()
                    or request.user.is_superuser)

    # def has_object_permission(self, request, view, obj):
    #     return request.user.is_admin
