from django.urls import path
from . import views as blog_views

urlpatterns = [
    path(route='blog', view=blog_views.blog, name='blog'),
    path(route='blog/<slug:category_slug>', view=blog_views.article_categories, name='article-categories'),
    path(route='blog/tags/<slug:tag_slug>', view=blog_views.article_tags, name='article-tags'),
    path(route='blog/<slug:category_slug>/<slug:article_slug>', view=blog_views.article_details,
         name='article-details'),
    path(route='blog/<slug:category_slug>/<slug:article_slug>/add-comment', view=blog_views.add_comment,
         name='add-comment'),
    path(route='blog/<slug:category_slug>/<slug:article_slug>/edit-comment', view=blog_views.edit_comment,
         name='edit-comment'),
    path(route='blog/<slug:category_slug>/<slug:article_slug>/delete-comment', view=blog_views.delete_comment,
         name='delete-comment'),
    path(route='blog/<slug:category_slug>/<slug:article_slug>/give-like', view=blog_views.give_like, name='give-like'),
    path(route='blog/<slug:category_slug>/<slug:article_slug>/give-dislike', view=blog_views.give_dislike,
         name='give-dislike'),
    path(route='blog-results', view=blog_views.blog_results, name='blog-results'),
]
