from rest_framework import permissions

# denies access when account is already linked to a venue account
class IsNotLinkedYet(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):

        if len(request.user.venue_profile.all()) > 0:
            return False

        return True
