from django.urls import path
from . import views

urlpatterns = [
    path(
        route="api/v1/users",
        view=views.UsersAPIView.as_view(),
        name="api-users"),
    path(
        route="api/v1/users/<int:pk>",
        view=views.UserDetailsAPIView.as_view(),
        name="api-v1-users-user-details",
    ),
    path(
        route="api/v1/users/individuals",
        view=views.IndividualProfileAPIView.as_view(),
        name="api-v1-users-individuals",
    ),
    path(
        route="api/v1/users/business",
        view=views.BusinessProfileAPIView.as_view(),
        name="api-v1-users-business",
    ),
    path(
        route="api/v1/users/individuals/<int:pk>",
        view=views.UserIndividualProfileDetailsAPIView.as_view(),
        name="api-v1-users-user-individuals-details",
    ),
]
