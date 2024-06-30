from django.contrib import admin
from .models import Newsletter, ContactMail


@admin.register(Newsletter)
class AdminNewsletter(admin.ModelAdmin):
    """
    Admin options and functionalities for Newsletter model.
    """

    list_display = ["id", "email", "subscribed_at"]
    list_filter = ["subscribed_at"]
    list_editable = ["email"]
    list_display_links = ["id"]
    search_fields = ["email"]
    ordering = ["subscribed_at"]
    fieldsets = [
        [
            "E-mail Subscriber:",
            {
                "fields": [
                    "email",
                ]
            },
        ],
    ]


@admin.register(ContactMail)
class AdminContactMail(admin.ModelAdmin):
    """
    Admin options and functionalities for ContactMail model.
    """

    list_display = ["id", "date_sent", "full_name", "phone_number", "email", "content"]
    list_filter = ["date_sent", "full_name", "email"]
    list_display_links = ["id"]
    search_fields = ["full_name", "email"]
    ordering = ["date_sent"]
    fieldsets = [
        [
            "Date Sent:",
            {
                "fields": [
                    "date_sent",
                ]
            },
        ],
        [
            "Sender Informations:",
            {
                "fields": [
                    "full_name",
                    "email",
                    "phone_number",
                ]
            },
        ],
        [
            "E-mail Content",
            {
                "fields": [
                    "content",
                ]
            },
        ],
    ]
