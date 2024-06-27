from django.urls import path
from . import views

urlpatterns = [
    path(
        route="api/v1/properties",
        view=views.PropertyAPIView.as_view(),
        name="api-v1-properties",
    ),
    path(
        route="api/v1/property-tour-schedules",
        view=views.TourScheduleAPIView.as_view(),
        name="api-v1-property-tour-schedules",
    ),
    path(
        route="api/v1/property-reviews",
        view=views.ReviewAPIView.as_view(),
        name="api-v1-property-reviews",
    ),
    path(
        route="api/v1/properties/<int:pk>",
        view=views.PropertyDetailAPIView.as_view(),
        name="api-v1-properties-property-details"
    )
]
