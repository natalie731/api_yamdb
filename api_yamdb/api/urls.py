from django.urls import include, path

from .views import AuthViewSet, TokenView


auth_patterns = [
    path('signup/', AuthViewSet.as_view()),
    path('token/', TokenView.as_view()),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
]
