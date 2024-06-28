from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from blog.models import Article, Comment
from django_filters.rest_framework import DjangoFilterBackend


class ArticlesAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "category__id": ["exact"],
        "category__name": ["exact"],
    }

    def get_view_name(self):
        return "Global Estate Hub Articles"


class ArticleDetailsAPIView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_view_name(self):
        return "Article Details"


class CommentsAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "user": ["exact"],
        "user__username": ["exact"],
        "article": ["exact"],
        "article__title": ["exact"],
        "active": ["exact"],
        "level": ["exact"],
    }

    def get_view_name(self):
        return "Global Estate Hub Comments"


class CommentDetailsAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_view_name(self):
        return "Comment Details"
