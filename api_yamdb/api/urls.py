from django.urls import include, path

from rest_framework import DefaultRouter


from .views import GenreViewSet, CategoryViewSet, TitlesViewSet, UserViewSet, CommentViewSet, ReviewViewSet, AuthViewSet, TokenView


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

auth_patterns = [
    path('signup/', AuthViewSet.as_view()),
    path('token/', TokenView.as_view()),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_patterns)),
]
