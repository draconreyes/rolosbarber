from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        is_authenticated = user and user.is_authenticated
        is_admin = user.is_admin if is_authenticated else False
        
        logger.info(f"IsAdminUser check - User: {user.username if is_authenticated else 'Anonymous'}")
        logger.info(f"  - is_authenticated: {is_authenticated}")
        logger.info(f"  - role: {user.role if is_authenticated else 'N/A'}")
        logger.info(f"  - is_admin property: {is_admin}")
        logger.info(f"  - Permission granted: {is_authenticated and is_admin}")
        
        return is_authenticated and is_admin


class IsClientUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_client


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or obj.client == request.user
