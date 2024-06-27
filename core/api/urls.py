from django.urls import path
from . import views

urlpatterns = [
    path(route="api/v1", view=views.api_endpoints, name="api-v1"),
    path(
        route="api/v1/newsletters",
        view=views.NewsletterAPIView.as_view(),
        name="api-newsletters",
    ),
]
