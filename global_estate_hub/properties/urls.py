from django.urls import path
from . import views as properties_views

urlpatterns = [
    path(route='add-property', view=properties_views.add_property, name='add-property'),
]
