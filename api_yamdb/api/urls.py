from django.urls import path

from .views import UserViewSet

urlpatterns = [
    path('v1/auth/signup/', UserViewSet.as_view()),
]
