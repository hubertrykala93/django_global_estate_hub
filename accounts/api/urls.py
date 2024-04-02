from django.urls import path
from . import views

urlpatterns = [
    path(route='api', view=views.api_endpoints, name='api'),
    path(route='api/v1/users', view=views.UsersAPIView.as_view(), name='api-users'),
    path(route='api/v1/users/profiles', view=views.ProfilesAPIView.as_view(), name='api=users=profiles'),
    path(route='api/v1/users/<int:pk>', view=views.UserDetailsAPIView.as_view(), name='api-users-user-details'),
    # path(route='api/v1/users/create', view=views.UserCreateAPIView.as_view(), name='api-users-user-create'),
    # path(route='api/v1/users/<int:pk>/update', view=views.UserUpdateAPIView.as_view(), name='api-users-user-update'),
    # path(route='api/v1/users/<int:pk>/delete', view=views.UserDeleteAPIView.as_view(), name='api-users-user-delete'),
    # path(route='api/v1/users/individuals', view=views.IndividualProfileAPIView.as_view(),
    #      name='api-users-individuals'),
    # path(route='api/v1/users/business', view=views.BusinessProfileAPIView.as_view(), name='api-users-business'),
]
