from django.urls import path

from . import views
from rest_framework.routers import DefaultRouter
urlpatterns = [

]


router  = DefaultRouter()
router.register('users', views.UserApiViewSet)
router.register('resources', views.ResourceManagementViewSet)
router.register('requests', views.RequestResourceViewSet)
router.register('message', views.MessageViewSet)
router.register('rating', views.RatingViewSet)




urlpatterns += router.urls

