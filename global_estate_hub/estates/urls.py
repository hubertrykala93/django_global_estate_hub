from django.urls import path
from . import views as estates_views

urlpatterns = [
    path(route='', view=estates_views.index, name='index'),
    path(route='about', view=estates_views.about, name='about'),
    path(route='properties', view=estates_views.properties, name='properties'),
    path(route='pages', view=estates_views.pages, name='pages'),
    path(route='blog', view=estates_views.blog, name='blog'),
    path(route='contact', view=estates_views.contact, name='contact'),
    path(route='get', view=estates_views.get_request, name='get'),
    path(route='post', view=estates_views.post_request, name='post'),
]
