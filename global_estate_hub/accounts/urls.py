from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path(route='sign-up/', view=accounts_views.sign_up, name='sign-up'),
]
