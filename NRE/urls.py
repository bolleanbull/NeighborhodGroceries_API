
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resources.urls')),
    path('api/token/', TokenObtainPairView.as_view(),name='token'),
    path('api/refresh/', TokenRefreshView.as_view(),name='refresh'),


]
