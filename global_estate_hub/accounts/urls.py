from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path(route='register', view=accounts_views.register, name='register'),
    path(route='login', view=accounts_views.login, name='login')
]
