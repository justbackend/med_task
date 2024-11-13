from functools import wraps

from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


def required_permission(required_permission_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):

            if required_permission_name:
                permissions = cache.get(f'permissions_{request.user.id}')

                if permissions is None:
                    raise PermissionDenied(detail="Get permission from getme/ endpoint")
                elif required_permission_name not in permissions:
                    return Response(
                        {"detail": "You do not have permissions to perform this action."},
                        status=status.HTTP_403_FORBIDDEN
                    )

            return view_func(self, request, *args, **kwargs)

        return _wrapped_view

    return decorator


class HasRequiredPermission(BasePermission):
    def __init__(self, perm):
        self.perm = perm

    def has_permission(self, request, view):
        permissions = cache.get(f'permissions_{request.user.id}')
        if permissions is None:
            raise PermissionDenied(detail="Get permissions from getme/ endpoint")
        return self.perm in permissions


class PermissionRequired(BasePermission):

    def has_permission(self, request, view):
        permissions = cache.get(f'permissions_{request.user.id}')
        if permissions is None:
            raise PermissionDenied(detail="Get permissions from getme/ endpoint")

        required_permission_codename = getattr(view, 'required_permission_codename', None)

        if not required_permission_codename:
            raise PermissionDenied(detail="Permission codename is not defined on the view.")
        return required_permission_codename in permissions
