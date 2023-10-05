from rest_framework import permissions

class TicketPermissions(permissions.BasePermission):

    def has_permission(self, request, view):

        if len(request.user.venue.all()) == 1:
            return True
        return False
