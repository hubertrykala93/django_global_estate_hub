from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Profile, OneTimePassword

admin.site.unregister(Group)


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['username', 'email', 'image', 'password', 'one_time_password', 'is_staff', 'is_active',
                    'is_superuser', 'date_joined']
    list_editable = ['email', 'is_staff', 'is_active', 'is_superuser']
    list_filter = ['username', 'email', 'date_joined']
    list_display_links = ['username']


@admin.register(OneTimePassword)
class AdminOneTimePassword(admin.ModelAdmin):
    list_display = ['user', 'password', 'created_at', 'expires_in']


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'gender', 'country', 'province', 'city']
    list_editable = ['first_name', 'last_name', 'gender', 'country', 'province', 'city']
    list_filter = ['last_name', 'country', 'province', 'city']
