from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path(route='register', view=accounts_views.register, name='register'),
    path(route='create-user', view=accounts_views.create_user, name='create-user'),
    path(route='login', view=accounts_views.log_in, name='login'),
    path(route='logout', view=accounts_views.log_out, name='logout'),
]
