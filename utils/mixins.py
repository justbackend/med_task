from utils.permissions import HasRequiredPermission

class ViewsetPermissionMixin:
    action_permissions = {}

    def get_permissions(self):
        permission = self.action_permissions.get(self.action)
        if permission is None:
            return []
        return [HasRequiredPermission(perm=permission)]


class APIViewPermissionMixin:
    method_permissions = {}

    def get_permissions(self):
        permission = self.method_permissions.get(self.request.method, None)
        if permission is None:
            return []
        return [HasRequiredPermission(perm=permission)]
