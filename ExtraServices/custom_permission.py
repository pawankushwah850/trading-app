from rest_framework.permissions import BasePermission


class OwnerReadWriteOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        return bool(request.user == obj.postOwner)

class CanTrade(BasePermission):

    def has_object_permission(self, request, view, obj):
        return True
