from rest_framework import permissions


class OwnerPerms(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view, obj) and request.user == obj


class CommentOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and request.user == obj.user