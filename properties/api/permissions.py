from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

        raise PermissionDenied(detail={
            "message": "To create, modify, or delete an object, you must be an administrator.",
        })
