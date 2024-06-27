from django.urls import path
from . import views

urlpatterns = [
    path(
        route="api/v1/properties",
        view=views.PropertyAPIView.as_view(),
        name="api-v1-properties",
    ),
    path(
        route="api/v1/properties/<int:pk>",
        view=views.PropertyDetailAPIView.as_view(),
        name="api-v1-properties-property-details",
    ),
    path(
        route="api/v1/properties/tour-schedules",
        view=views.TourScheduleAPIView.as_view(),
        name="api-v1-properties-tour-schedules",
    ),
    path(
        route="api/v1/properties/tour-schedules/<int:pk>",
        view=views.TourScheduleDetailAPIView.as_view(),
        name="api-v1-properties-tour-schedules-details",
    ),
    path(
        route="api/v1/properties/reviews",
        view=views.ReviewAPIView.as_view(),
        name="api-v1-properties-reviews",
    ),
    path(
        route="api/v1/properties/reviews/<int:pk>",
        view=views.ReviewDetailAPIView.as_view(),
        name="api-v1-properties-reviews-details",
    ),
]
