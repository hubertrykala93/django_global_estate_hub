from django.urls import path
from . import views as estates_views

urlpatterns = [
    path(route='', view=estates_views.index, name='index'),
    path(route='about', view=estates_views.about, name='about'),
    path(route='properties', view=estates_views.properties, name='properties'),
    path(route='pages', view=estates_views.pages, name='pages'),
    path(route='blog', view=estates_views.blog, name='blog'),
    path(route='contact', view=estates_views.contact, name='contact'),
    path(route='properties/estate-details', view=estates_views.estate, name='estate-details'),
    path(route='properties/estate-details/detail', view=estates_views.detail, name='detail')
]
