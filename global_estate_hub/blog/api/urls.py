from django.urls import path
from . import views

urlpatterns = [
    path(route='api/articles', view=views.ArticleAPIView.as_view(), name='api-articles'),
    path(route='api/article-comments', view=views.CommentAPIView.as_view(), name='api-article-comments'),
]
