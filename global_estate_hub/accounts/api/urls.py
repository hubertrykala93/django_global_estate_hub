from django.urls import path
from . import views

urlpatterns = [
    path(route='api/users', view=views.UserAPIView.as_view(), name='api-users'),
    path(route='api/individual-profiles', view=views.IndividualProfileAPIView.as_view(),
         name='api-individual-profiles'),
    path(route='api/business-profiles', view=views.BusinessProfileAPIView.as_view(), name='api-business-profiles'),
]
