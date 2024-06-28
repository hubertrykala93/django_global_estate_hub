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
        route="api/v1/tour-schedules",
        view=views.TourSchedulesAPIView.as_view(),
        name="api-v1-tour-schedules",
    ),
    path(
        route="api/v1/tour-schedules/<int:pk>",
        view=views.TourScheduleDetailAPIView.as_view(),
        name="api-v1-tour-schedules-details",
    ),
    path(
        route="api/v1/reviews",
        view=views.ReviewsAPIView.as_view(),
        name="api-v1-reviews",
    ),
    path(
        route="api/v1/reviews/<int:pk>",
        view=views.ReviewDetailAPIView.as_view(),
        name="api-v1-review-details",
    ),
]
