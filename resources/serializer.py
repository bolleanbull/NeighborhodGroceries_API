
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import(
    Profile,
    Resource, 
    RequestResource,
    Rating,
    Message

)

class ProfileSerializerClass(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'name', 
            'age', 
            'gender',
            'user_role',
            'phone',
            'address'
        ]

class UserSerializerClass(serializers.ModelSerializer):

    profile = ProfileSerializerClass(required=False)
    user_id = serializers.IntegerField(source='id', read_only=True)
    
    class Meta:
        model = User
        fields = ['user_id','username', 'email','password','profile']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }
        read_only_fields = ['user_id']


    def create(self, validated_data):
        
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        profile = Profile(**profile_data, user=user)
        profile.save()
        return user
    
    def update(self, instance, validated_data):
        
        profile_data = validated_data.pop('profile')

        instance.username = validated_data.get('username', instance.username)
        instance.set_password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile = instance.profile  
        profile.name=profile_data.get('name', profile.name)
        profile.address = profile_data.get('address',profile.address)
        profile.save()
        return instance
    
class ResourceSerializerClass(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()
    resource_id  = serializers.IntegerField(source='id', read_only=True)
    class Meta: 
        model = Resource
        fields = [
            'resource_id',
            'owner',
            'name', 
            'condition',
            'day_price',
            'availabel',
            'location',
            'description',
            'uploaded_on',

        ]
        read_only_fields  = ['owner', 'availabel', 'uploaded_on']

    def create(self, validated_data):
        user = self.context['user']
        return Resource.objects.create(**validated_data,owner=user)
    
    



class RequestResourceSerializerClass(serializers.ModelSerializer):
    request_user = serializers.IntegerField(source="user.id", read_only=True)
    resource_id = serializers.IntegerField(write_only=True)
    resource = ResourceSerializerClass(read_only=True)
    object_id = serializers.IntegerField(source='id', read_only=True)

    

    class Meta: 
        model = RequestResource
        fields = [
            'object_id',
            "request_user",
            "resource_id",
            "resource",
            "duration_in_days", 
            "starting_date",
            "end_date",
            "status",
        ]
        read_only_fields = ['status']

    def create(self, validated_data):
        user = self.context['user']
        resource_id = validated_data.pop('resource_id')
        resource = get_object_or_404(Resource, pk=resource_id)

        requestResource = RequestResource.objects.create(user=user, resource=resource, **validated_data)
        return requestResource
    


class MessageSerializer(serializers.ModelSerializer):

    
    resource = serializers.SlugRelatedField(slug_field="name", read_only=True)
    resource_id = serializers.IntegerField(write_only=True)


    class Meta:
        model = Message
        fields = [
            'resource',
            'text', 
            'on_date',
            'resource_id'
        ]
        read_only_fields =['on_date','resource']


    def create(self, validated_data):
        
        sender = self.context['user']
        resource_id = validated_data.get('resource_id')
        message = validated_data.get('text')
        resource = get_object_or_404(Resource,pk=resource_id)

        return Message.objects.create(resource=resource, text=message, sender=sender)
    

class RatingSerializerClass(serializers.ModelSerializer):

    resource_id  = serializers.IntegerField(write_only=True)
    item = serializers.CharField(source='resource.name', read_only=True)
    by = serializers.CharField(source='user.profile.name', read_only=True)
    class Meta:
        model = Rating
        fields = [
            'item',
            'by',
            'resource_id',
            'like',
            "feedback"
        ]

    def create(self, validated_data):
       
       user = self.context['user']
       resource_id = validated_data.get('resource_id')
       like  = validated_data.get('like')
       feedback= validated_data.get('feedback')
       resource = Resource.objects.get(pk=resource_id)

       return Rating.objects.create(user=user, resource=resource, like=like, feedback=feedback)