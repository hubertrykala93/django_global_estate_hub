from django.urls import path
from .views import UserList, IndividualProfileList, BusinessProfileList

urlpatterns = [
    path(route='api/users', view=UserList.as_view(), name='api-users'),
    path(route='api/individual-profiles', view=IndividualProfileList.as_view(), name='api-individual-profiles'),
    path(route='api/business-profiles', view=BusinessProfileList.as_view(), name='api-business-profiles'),
]
