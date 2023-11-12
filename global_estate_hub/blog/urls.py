from django.urls import path
from . import views as blog_views

urlpatterns = [
    path(route='blog', view=blog_views.blog, name='blog'),
    path(route='blog/<slug:category_slug>', view=blog_views.article_categories, name='article-category'),
    path(route='blog/<slug:category_slug>/<slug:article_slug>', view=blog_views.article_details,
         name='article-details'),
]
