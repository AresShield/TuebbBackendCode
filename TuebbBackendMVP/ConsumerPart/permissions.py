from rest_framework.permissions import BasePermission

class HasPermissionToCreateAccount(BasePermission):
    def has_permission(self, request, view):
        #print(len(request.user.consumer_account.all())==0)
        if len(request.user.consumer_account.all())==0:
            return True
        return False

class IsCreator(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
