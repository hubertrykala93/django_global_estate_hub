from django.urls import path
from . import views

urlpatterns = [
    path(route="api", view=views.api_endpoints, name="api"),
    path(route="api/v1/users", view=views.UsersAPIView.as_view(), name="api-users"),
    path(
        route="api/v1/users/<int:pk>",
        view=views.UserDetailsAPIView.as_view(),
        name="api-users-user-details",
    ),
    path(
        route="api/v1/users/create",
        view=views.UserCreateAPIView.as_view(),
        name="api-users-create",
    ),
    path(
        route="api/v1/users/<int:pk>/update",
        view=views.UserUpdateAPIView.as_view(),
        name="api-users-user-update",
    ),
    path(
        route="api/v1/users/<int:pk>/delete",
        view=views.UserDeleteAPIView.as_view(),
        name="api-users-user-delete",
    ),
    path(
        route="api/v1/users/individuals",
        view=views.IndividualProfileAPIView.as_view(),
        name="api-users-individuals",
    ),
    path(
        route="api/v1/users/business",
        view=views.BusinessProfileAPIView.as_view(),
        name="api-users-business",
    ),
    path(
        route="api/v1/users/individuals/<int:pk>",
        view=views.UserIndividualProfileDetailsAPIView.as_view(),
        name="api-users-user-individuals-details",
    ),
    path(
        route="api/v1/users/individuals/<int:pk>/update",
        view=views.UserIndividualProfileUpdateAPIView.as_view(),
        name="api-users-user-individuals-update",
    ),
    path(
        route="api/v1/users/individuals/<int:pk>/delete",
        view=views.UserIndividualProfileDeleteAPIView.as_view(),
        name="api-users-user-individuals-delete",
    ),
    path(
        route="api/v1/users/business/<int:pk>",
        view=views.UserBusinessProfileDetailsAPIView.as_view(),
        name="api-users-user-business-details",
    ),
    path(
        route="api/v1/users/business/<int:pk>/update",
        view=views.UserBusinessProfileUpdateAPIView.as_view(),
        name="api-users-user-business-update",
    ),
    path(
        route="api/v1/users/business/<int:pk>/delete",
        view=views.UserBusinessProfileDeleteAPIView.as_view(),
        name="api-users-user-business-delete",
    ),
]
