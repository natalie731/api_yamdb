from django.urls import include, path

from rest_framework import DefaultRouter

from .views import CommentViewSet, ReviewViewSet

from .views import GenreViewSet, CategoryViewSet, TitlesViewSet, UserViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('auth/signup', UserViewSet)
router_v1.register(r'categories', CategoryViewSet, basename='Category')
router_v1.register(r'genres', GenreViewSet, basename='Genre')
router_v1.register(r'titles', TitlesViewSet, basename='Title')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                   basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register('signup', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/auth/', include(router_v1.urls)),
]
