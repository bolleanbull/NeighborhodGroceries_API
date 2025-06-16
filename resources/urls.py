from django.urls import path

from . import views
from rest_framework.routers import DefaultRouter
urlpatterns = [

]


router  = DefaultRouter()
router.register('users', views.UserApiViewSet)
router.register('resources', views.ResourceManagementViewSet)


urlpatterns += router.urls

