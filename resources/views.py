from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import filters
from django_filters.rest_framework  import DjangoFilterBackend
from .filters import ResourceFilter
from rest_framework.pagination import PageNumberPagination




from rest_framework.decorators import action

from rest_framework.permissions import(
    IsAdminUser,
    IsAuthenticated, 
    IsAuthenticatedOrReadOnly,
    AllowAny
)

from .permissions import (
    IsAdminOrResourceOwner ,
    IsAdminOrRealUser, 
    IsAdminOrBorrower,
    NoManZone,


)


from .serializer import (
    UserSerializerClass,
    ResourceSerializerClass,
    RequestResourceSerializerClass, 
    MessageSerializer,
    RatingSerializerClass
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

    def get_permissions(self):
        
        if self.action=='create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminOrRealUser]

        return [permission() for permission in self.permission_classes]
    


class ResourceManagementViewSet(viewsets.ModelViewSet):

    throttle_scope  = 'resource'

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializerClass
    permission_classes = [IsAuthenticated]
    filter_backends= [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'owner__profile__name',"location"]
    ordering_fields = ['day_price','condition']
    filterset_class = ResourceFilter



    def get_permissions(self):
        
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
            
        else: 
            self.permission_classes = [IsAdminOrResourceOwner]
        return [permission() for permission in self.permission_classes]
    
    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context['user'] = self.request.user

        return context
    

class RequestResourceViewSet(viewsets.ModelViewSet):

    queryset = RequestResource.objects.all()
    serializer_class  =  RequestResourceSerializerClass
    permission_classes = [IsAuthenticated, IsAdminOrBorrower]


    def get_permissions(self):
        
        if self.request.method in ['PUT', 'PATCH' ]:
            self.permission_classes = [NoManZone]
            return [NoManZone()]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        qs =  super().get_queryset()
        if self.request.user.is_superuser:
            return qs 
        
        return qs.filter(user=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    @action(methods=['GET'],detail=False, url_path="my_resources_requests", url_name="my_resource_request", permission_classes=[IsAuthenticated])
    def my_resouces_request(self,request, *args, **kwargs):

        requests_resources = RequestResource.objects.select_related('resource').filter(resource__owner=request.user)
        print(requests_resources)
        serializer = RequestResourceSerializerClass(requests_resources, many=True)
        
        return  Response(serializer.data)
    
    @action(methods=['POST'],detail=True, url_name="request_action", permission_classes = [IsAdminOrResourceOwner])

    def request_action(self, request ,pk):

        request_obj = get_object_or_404(RequestResource, pk=pk)
   
        request_obj.status = request.data.get('action')
        request_obj.save()
        ## we are chaging the status of the resource here 
        resource = Resource.objects.get(pk=request_obj.resource.id)
        resource.availabel = False if request_obj.status=='Accepted' else True
        if not resource.availabel:
            resource.save()

        print(resource.availabel)

        serializer = RequestResourceSerializerClass(request_obj)
        return Response(serializer.data)
    



class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.select_related('resource')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        
        if not self.action in ['list', 'retrieve']:
            self.permission_classes= [IsAdminUser]
        return [permission() for permission in self.permission_classes]
    
    def get_queryset(self):
        qs= super().get_queryset()
        return qs.filter(resource__owner=self.request.user)

    def get_serializer_context(self):
        context  =  super().get_serializer_context()
        context['user'] = self.request.user

        return context
    

class RatingViewSet(viewsets.ModelViewSet):

    queryset  = Rating.objects.select_related('resource','user')
    serializer_class = RatingSerializerClass 

    def get_serializer_context(self):
        context  =  super().get_serializer_context()
        context['user'] = self.request.user
        return context
    def get_permissions(self):
    
        if not self.action in [ 'list','retrieve','create' ]:
            self.permission_classes = [NoManZone]
            return [NoManZone()]
        return [permission() for permission in self.permission_classes]




class LandAndBorrowHistoryViewSet(viewsets.ViewSet):

    permission_classes  = [IsAuthenticated]

    def list(self,request):
        # land  and borrow historry of  the user 
        published_resources = Resource.objects.select_related('owner').filter(owner=self.request.user)
        resources_request_accepted_ids  = list(RequestResource.objects.select_related('resource').filter(status='Accepted', resource__owner=self.request.user).values_list("resource__id", flat=True))

        borrowed_resources = Resource.objects.filter(id__in=resources_request_accepted_ids)

        # this is serialized data 
        publised_resources  = ResourceSerializerClass(published_resources, many=True).data
        borrowed_resources = ResourceSerializerClass(borrowed_resources, many=True).data

        return Response({
            'published_resources': publised_resources, 
            'borrowed_resources': borrowed_resources
        })
    














