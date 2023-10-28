from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User

admin.site.unregister(Group)


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active', 'is_verified', 'is_superuser']
    list_editable = ['username', 'email', 'is_staff', 'is_active', 'is_verified', 'is_superuser']
    list_filter = ['username', 'email', 'date_joined']
    list_display_links = None
