from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    message = {
        'message': 'Access is granted only to administrators of the Global Estate Hub page.',
    }

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True

        return False
