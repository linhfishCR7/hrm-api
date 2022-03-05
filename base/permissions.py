# Python imports

# Rest framework imports
from rest_framework.permissions import BasePermission

# Application imports
from base.templates.error_templates import ErrorTemplate
from base.utils import print_value


class IsAdmin(BasePermission):
    message = ErrorTemplate.AuthorizedError.ADMIN_REQUIRED

    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_active and request.user.is_superuser


class IsHrm(BasePermission):
    message = ErrorTemplate.AuthorizedError.HRM_REQUIRED

    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_active

class IsUser(BasePermission):
    message = ErrorTemplate.AuthorizedError.USER_REQUIRED

    def has_permission(self, request, view):
        return request.user.id and request.user.is_active