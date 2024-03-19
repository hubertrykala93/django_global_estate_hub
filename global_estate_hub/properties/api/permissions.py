from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """
    The function only allows administrators of the Global Estate Hub website to access the properties API.
    """
    message = {
        'message': 'Access is granted only to administrators of the Global Estate Hub page.',
    }

    def has_permission(self, request, view):
        """
        Checks whether the user is a superuser. If so, they are granted permissions to access the properties API.

        return: bool
        """
        user = request.user

        if user.is_superuser:
            return True

        return False
