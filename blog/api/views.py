from .serializers import (
    ArticleSerializer,
    ArticleCreateSerializer,
    ArticleUpdateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    CategorySerializer,
    TagSerializer,
)
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from blog.models import Article, Comment, Category, Tag
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from django.utils.text import slugify
from datetime import datetime
from rest_framework.filters import OrderingFilter, SearchFilter
from .permissions import IsAdminOnly


class CategoryAPIView(ListAPIView):
    """
    API view allowing to retrieve all blog categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagsAPIView(ListAPIView):
    """
    API view allowing to retrieve all blog tags.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticlesAPIView(ListAPIView):
    """
    API view allowing to retrieve all articles.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = {
        "category__id": ["exact"],
        "category__name": ["exact"],
    }
    ordering_fields = ["date_posted", "title"]
    search_fields = ["title", "content"]

    def get_view_name(self):
        return "Global Estate Hub Articles"


class ArticleDetailsAPIView(RetrieveAPIView):
    """
    API view allowing to retrieve a specific article.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_view_name(self):
        return "Article Details"


class ArticleCreateApiView(CreateAPIView):
    """
    API view allowing to create a new article.
    """

    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Article Create"

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title")
        slug = slugify(title)
        serializer.save(slug=slug)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            headers = get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The article has been created successfully",
                    "article": serializer.data,
                    "headers": headers,
                },
                headers=headers,
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ArticleUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view allowing partial or full update of a specific Article object.
    """

    serializer_class = ArticleUpdateSerializer
    queryset = Article.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Article Update"

    def perform_update(self, serializer):
        title = serializer.validated_data.get("title")
        slug = slugify(title)
        serializer.save(slug=slug)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance, data=request.data
        )

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            headers = get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The article has been successfully updated.",
                    "article": serializer.data,
                    "headers": headers,
                },
                headers=headers,
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ArticleDeleteAPIView(RetrieveDestroyAPIView):
    """
    API view allowing deletion of a specific article.
    """

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Article Delete"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        temp_id = instance.id

        try:
            self.perform_destroy(instance=instance)

            return Response(
                data={
                    "message": "The article has been deleted successfully.",
                    "id": temp_id,
                    "deleted_by": self.request.user.username,
                    "deleted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception:
            return Response(
                data={"error": "There was an error while deleting the user."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CommentsAPIView(ListAPIView):
    """
    API view allowing to retrieve all comments.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "user__id": ["exact"],
        "user__username": ["exact"],
        "article__id": ["exact"],
        "article__title": ["exact"],
        "active": ["exact"],
        "level": ["exact"],
    }

    def get_view_name(self):
        return "Global Estate Hub Comments"


class CommentDetailsAPIView(RetrieveAPIView):
    """
    API view allowing to retrieve a specific comment.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_view_name(self):
        return "Comment Details"


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()
    lookup_field = "pk"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            headers = get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The comment has been created successfully.",
                    "comment": serializer.data,
                    "headers": headers,
                },
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


def get_success_headers(data):
    try:
        return {"location": str(data["id"])}
    except (TypeError, KeyError):
        return {}
