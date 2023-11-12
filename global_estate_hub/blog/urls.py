from django.urls import path
from . import views as blog_views

urlpatterns = [
    path(route='blog', view=blog_views.blog, name='blog'),
]
