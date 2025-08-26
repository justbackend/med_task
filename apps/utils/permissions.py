from rest_framework.permissions import BasePermission

from apps.users.models import User


class RolePermission(BasePermission):
    """
    Allows access only to users with roles in the view's `required_roles` attribute.
    """

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False

        allowed_roles = getattr(view, "allowed_roles", None)
        if allowed_roles is None:
            return True

        user_role = getattr(request.user, "role", None)
        if user_role == User.Role.ADMIN:
            return True
        return user_role in allowed_roles
