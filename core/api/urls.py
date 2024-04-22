from django.urls import path
from . import views

urlpatterns = [
    path(
        route="api/newsletters",
        view=views.NewsletterAPIView.as_view(),
        name="api-newsletters",
    ),
]
