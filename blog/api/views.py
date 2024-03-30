from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.generics import ListAPIView
from blog.models import Article, Comment


class ArticleAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_view_name(self):
        return 'Global Estate Hub Articles'

    def get_view_description(self, html=False):
        return 'API view with all articles on the Global Estate Hub platform.'


class CommentAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_view_name(self):
        return 'Global Estate Hub Article Comments'

    def get_view_description(self, html=False):
        return 'API view with all comments on the Global Estate Hub platform.'
