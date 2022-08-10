from django.urls import include, path
from rest_framework import routers

from .views import GenreViewSet, CategoryViewSet, TitlesViewSet, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('auth/signup', UserViewSet)
router_v1.register(r'categories', CategoryViewSet, basename='Category')
router_v1.register(r'genres', GenreViewSet, basename='Genre')
router_v1.register(r'titles', TitlesViewSet, basename='Title')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
