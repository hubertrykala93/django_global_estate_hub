from django.urls import path
from . import views as estates_views

urlpatterns = [
    path(route='', view=estates_views.index, name='index'),
    path(route='add-category', view=estates_views.add_category, name='add-category')
]
