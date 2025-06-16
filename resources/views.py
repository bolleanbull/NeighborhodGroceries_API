from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly


from .serializer import (
    UserSerializerClass,
    ResourceSerializerClass,
)
from .models import (
    Profile,
    RequestResource, 
    Resource, 
    Message, 
    Rating


)


from rest_framework import viewsets


class UserApiViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializerClass  
    permission_classes = [IsAuthenticated]


    def get_permissions(self):
        if self.action=='list':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
class ResourceManagementViewSet(viewsets.ModelViewSet):

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializerClass


    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context['user'] = self.request.user

        return context
    



