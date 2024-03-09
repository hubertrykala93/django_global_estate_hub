from django.urls import path
from .views import PropertyList

urlpatterns = [
    path(route='api/properties', view=PropertyList.as_view(), name='api-properties')
]
