from pyclbr import Class
from rest_framework.permissions import BasePermission, SAFE_METHODS  

class IsAdminOrReadOnly(BasePermission):
    ''' Returns True if the request is of type SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS') or if the requesting user is an admin'''
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff 