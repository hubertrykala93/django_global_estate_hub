from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView
from blog.models import Article, Comment, Tag
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status


class ArticlesAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__name', 'tags__name']

    def get_view_name(self):
        return 'Articles'


class ArticleDetailsAPIView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'

    def get_view_name(self):
        return 'Article Details'


class ArticleCreateAPIView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_view_name(self):
        return 'Article Create'

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        tags_data = data.pop('tags', None)
        image = data.pop('image', None)
        print(data)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            if image:
                serializer.validated_data['image'] = image

            self.perform_create(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['level', 'active']

    def get_view_name(self):
        return 'All Comments'


class CommentDetailsAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_view_name(self):
        return 'Comment Details'
