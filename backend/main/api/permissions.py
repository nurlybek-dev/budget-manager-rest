from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Allow only owner user
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
