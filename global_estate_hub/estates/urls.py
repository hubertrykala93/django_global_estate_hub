from django.urls import path
from . import views as estates_views

urlpatterns = [
    path(route='', view=estates_views.index, name='index'),
    path(route='about', view=estates_views.about, name='about'),
    path(route='properties', view=estates_views.properties, name='properties'),
    path(route='pages', view=estates_views.properties, name='pages'),
    path(route='blogs', view=estates_views.properties, name='blogs'),
    path(route='contact', view=estates_views.properties, name='contact'),
    path(route='add-category', view=estates_views.add_category, name='add-category'),
]
