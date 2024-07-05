from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

        raise PermissionDenied(
            detail={
                "message": "The page is accessible only to the administrator.",
            }
        )
