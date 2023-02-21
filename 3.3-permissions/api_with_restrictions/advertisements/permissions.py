import permission as permission
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user)
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.creator

# class IsAdmin(BasePermission):
#     def hes_object_permission(self,request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return bool(request.user and request.user.is_staff)