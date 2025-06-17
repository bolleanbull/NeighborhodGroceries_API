from rest_framework.permissions import BasePermission
from rest_framework import permissions





class IsAdminOrObjectOwner(BasePermission):

    def __init__(self ,owner=None):
        self.owner = owner

    def has_object_permission(self, request, view, obj):    
        return request.user.is_superuser or getattr(obj, self.owner)==request.user 
    
    

class IsAdminOrRealUser(BasePermission):

    def  has_object_permission(self, request, view, obj):    
        return request.user.id==obj.id or request.user.is_superuser 
    



class IsAdminOrResourceOwner(IsAdminOrObjectOwner):

    def __init__(self):
        super().__init__('owner')


class IsAdminOrBorrower(IsAdminOrObjectOwner):

    def __init__(self):
        super().__init__("user")


class NoManZone(BasePermission):

    def has_object_permission(self, request, view, obj):
        return False
    
    


