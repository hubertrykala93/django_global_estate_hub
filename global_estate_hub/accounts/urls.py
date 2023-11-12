from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path(route='register', view=accounts_views.register, name='register'),
    path(route='create-user', view=accounts_views.create_user, name='create-user'),
    path(route='login', view=accounts_views.log_in, name='login'),
    path(route='logout', view=accounts_views.log_out, name='logout'),
    path(route='account-settings', view=accounts_views.account_settings, name='account-settings'),
    path(route='forget-password', view=accounts_views.forget_password, name='forget-password'),
    path(route='send-password', view=accounts_views.send_password, name='send-password'),
    path(route='validate-password', view=accounts_views.validate_password, name='validate-password'),
    path(route='set-password', view=accounts_views.set_password, name='set-password'),
]
