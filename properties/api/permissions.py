from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

        raise PermissionDenied(detail={
            "message": "To create, modify, or delete an object, you must be an administrator.",
        })


class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        if isinstance(view, CreateAPIView):
            if request.user.is_authenticated:
                return True

            if request.user.is_authenticated and request.user.is_staff:
                return True

            raise PermissionDenied(
                detail={
                    "message": "To create a new object, you must be an administrator.",
                }
            )

        if isinstance(view, ListAPIView):
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_staff:
            return True

        if obj == request.user:
            return True

        if obj.user == request.user:
            return True

        raise PermissionDenied(
            detail={
                "message": "To modify or delete the object, you must be its owner or an administrator.",
            }
        )
