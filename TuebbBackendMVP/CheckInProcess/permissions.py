from rest_framework import permissions

class TicketPermissions(permissions.BasePermission):

    def has_permission(self, request, view):

        if len(request.user.venue.all()) == 1:
            return True
        return False


class TicketReadPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if obj.paid == False:
            return True

        if obj.paid == True:
            if request.user == obj.owner or request.user == obj.creator:
                return True
        return False

class TicketBuyPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if obj.paid == True:
            return False

        if len(request.user.consumer_account.all()) == 1:
            return True

        return False
