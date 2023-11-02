from django.contrib import admin
from .models import Newsletter


@admin.register(Newsletter)
class AdminNewsletter(admin.ModelAdmin):
    list_display = ['email']
