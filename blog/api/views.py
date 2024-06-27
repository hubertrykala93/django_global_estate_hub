from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from blog.models import Article, Comment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status


class ArticlesAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category__name", "tags__name"]

    def get_view_name(self):
        return "Articles"


class ArticleDetailsAPIView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "pk"

    def get_view_name(self):
        return "Article Details"


class CommentsAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["level", "active", "user__username", "user__id", "article__id", "article__slug"]

    def get_view_name(self):
        return "All Comments"


class CommentDetailsAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_view_name(self):
        return "Comment Details"
