from django.contrib import admin
from .models import Newsletter


@admin.register(Newsletter)
class AdminNewsletter(admin.ModelAdmin):
    list_display = ['email']
    list_editable = ['email']
    list_filter = ['email']
    list_display_links = None
