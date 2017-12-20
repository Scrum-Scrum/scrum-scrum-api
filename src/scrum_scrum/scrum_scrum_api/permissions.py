from rest_framework import permissions

class UpdateOwnUser(permissions.BasePermission):
    """Allow users to edit their own information."""

    def has_object_permission(self, request, view, obj):
        """Verify that a user is trying to change their own info."""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id
