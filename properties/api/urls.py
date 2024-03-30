from django.urls import path
from . import views

urlpatterns = [
    path(route='api/properties', view=views.PropertyAPIView.as_view(), name='api-properties'),
    path(route='api/property-tour-schedules', view=views.TourScheduleAPIView.as_view(),
         name='api-property-tour-schedules'),
    path(route='api/property-reviews', view=views.ReviewAPIView.as_view(), name='api-property-reviews')
]
