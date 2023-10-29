from rest_framework.routers import DefaultRouter
from django.urls.conf import include
from django.urls import re_path, path

from .viewsets import UserViewSet
from .views import LoginView

router = DefaultRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)
urlpatterns = [
    re_path('', include(router.urls)),
    path('login', LoginView.as_view(), name='login')
]
