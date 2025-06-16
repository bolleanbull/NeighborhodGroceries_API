from django.contrib import admin

# Register your models here.
from .models import (
    Profile,
    RequestResource, 
    Resource,
    Message, 
    Rating

)

admin.site.register(Profile)
admin.site.register(RequestResource)
admin.site.register(Resource)
admin.site.register(Rating)
admin.site.register(Message)
