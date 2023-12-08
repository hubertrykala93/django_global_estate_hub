from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path(route='register', view=accounts_views.register, name='register'),
    path(route='create-user', view=accounts_views.create_user, name='create-user'),
    path(route='activate/<uidb64>/<token>', view=accounts_views.activate, name='activate'),
    path(route='login', view=accounts_views.log_in, name='login'),
    path(route='authorization', view=accounts_views.authorization, name='authorization'),
    path(route='logout', view=accounts_views.log_out, name='logout'),
    path(route='account-settings', view=accounts_views.account_settings, name='account-settings'),
    path(route='user-settings', view=accounts_views.user_settings, name='user-settings'),
    path(route='profile-settings', view=accounts_views.profile_settings, name='profile-settings'),
    path(route='localization-settings', view=accounts_views.localization_settings, name='localization-settings'),
    path(route='social-media-settings', view=accounts_views.social_media_settings, name='social-media-settings'),
    path(route='forget-password', view=accounts_views.forget_password, name='forget-password'),
    path(route='send-password', view=accounts_views.send_password, name='send-password'),
    path(route='validate-password', view=accounts_views.validate_password, name='validate-password'),
    path(route='set-password', view=accounts_views.set_password, name='set-password'),
]
