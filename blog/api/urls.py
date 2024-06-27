from django.urls import path
from . import views

urlpatterns = [
    path(
        route="api/v1/articles",
        view=views.ArticlesAPIView.as_view(),
        name="api-articles",
    ),
    path(
        route="api/v1/articles/<int:pk>",
        view=views.ArticleDetailsAPIView.as_view(),
        name="api-articles-article-details",
    ),
    path(
        route="api/v1/comments",
        view=views.CommentsAPIView.as_view(),
        name="api-comments",
    ),
    path(
        route="api/v1/comments/<int:pk>",
        view=views.CommentDetailsAPIView.as_view(),
        name="api-comments-comment-details",
    ),
]
