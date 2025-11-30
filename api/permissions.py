from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    """
    Доступ разрешен только пользователям из группы Manager
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()


class IsClient(BasePermission):
    """
    Доступ разрешен только пользователям из группы Manager
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Client').exists()