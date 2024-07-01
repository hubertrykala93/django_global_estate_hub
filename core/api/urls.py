from django.urls import path
from . import views

urlpatterns = [
    path(route="api/v1", view=views.api_endpoints, name="api-v1"),
    path(
        route="api/v1/newsletters",
        view=views.NewsletterAPIView.as_view(),
        name="api-v1-newsletters",
    ),
    path(
        route="api/v1/newsletters/<int:pk>",
        view=views.NewsletterDetailsAPIView.as_view(),
        name="api-v1-newsletters-newsletter-details",
    ),
    path(
        route="api/v1/newsletters/create-newsletter",
        view=views.NewsletterCreateAPIView.as_view(),
        name="api-v1-newsletters-create-newsletter",
    ),
    path(
        route="api/v1/newsletters/update-newsletter/<int:pk>",
        view=views.NewsletterUpdateAPIView.as_view(),
        name="api-v1-newsletters-update-newsletter",
    ),
    path(
        route="api/v1/newsletters/delete-newsletter/<int:pk>",
        view=views.NewsletterDeleteAPIView.as_view(),
        name="api-v1-newsletters-delete-newsletter",
    ),
]
