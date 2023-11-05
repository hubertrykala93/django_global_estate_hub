from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User

admin.site.unregister(Group)


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['username', 'email', 'password', 'is_staff', 'is_active', 'is_superuser',
                    'date_joined']
    list_editable = ['is_staff', 'is_active', 'is_superuser']
    list_filter = ['username', 'email', 'date_joined']
    list_display_links = None
