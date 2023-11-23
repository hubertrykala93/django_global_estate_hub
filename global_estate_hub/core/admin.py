from django.contrib import admin
from .models import Newsletter, ContactMail


@admin.register(Newsletter)
class AdminNewsletter(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
    list_editable = ['email']
    list_display_links = None


@admin.register(ContactMail)
class AdminContactMail(admin.ModelAdmin):
    list_display = ['date_sent', 'full_name', 'phone_number', 'email', 'content']
    list_filter = ['date_sent', 'full_name', 'email']
    list_display_links = ['full_name']
