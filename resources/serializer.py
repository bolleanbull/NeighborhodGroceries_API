

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

    profile = ProfileSerializerClass()
    user_id = serializers.IntegerField(source='id')
    
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
    class Meta: 
        model = Resource
        fields = [
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
    
    
    





    




