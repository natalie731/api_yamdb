from django.shortcuts import render
from rest_framework import filters, viewsets
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated


from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (CommentSerializer, ReviewSerializer)
# from .permissions import IsAuthorOrReadOnly
from reviews.models import Review, Comment


class ReviewViewSet(viewsets.ModelViewSet):
    pass
    # queryset = Review.objects.all()
    # serializer_class = PostSerializer
    # permission_classes = [IsAuthorOrReadOnly]
    # pagination_class = LimitOffsetPagination
    # filter_backends = (DjangoFilterBackend,)
    #
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    pass
    # serializer_class = CommentSerializer
    # permission_classes = [IsAuthorOrReadOnly]
    #
    # def get_queryset(self):
    #     post = get_object_or_404(Review, id=self.kwargs.get("post_id"))
    #     new_queryset = post.comments.all()
    #     return new_queryset
    #
    # def perform_create(self, serializer):
    #     post = get_object_or_404(Review, id=self.kwargs.get("post_id"))
    #     serializer.save(author=self.request.user, post=post)
