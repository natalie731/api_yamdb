from django.urls import path

from .views import TokenView, UserViewSet

urlpatterns = [
    path('v1/auth/signup/', UserViewSet.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
]
