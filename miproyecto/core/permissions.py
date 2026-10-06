from rest_framework.permissions import BasePermission, SAFE_METHODS


class PrendaPermission(BasePermission):
    """Los usuarios autenticados leen/escriben; solo staff puede eliminar."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method == 'DELETE':
            return request.user.is_staff
        return request.method in SAFE_METHODS or request.method in {
            'POST', 'PUT', 'PATCH'
        }
