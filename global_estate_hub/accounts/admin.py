from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, OneTimePassword, Individual, Business

admin.site.unregister(Group)


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['username', 'email', 'image', 'password', 'account_type', 'is_verified', 'is_staff',
                    'is_active', 'is_superuser', 'date_joined', 'last_login']
    list_editable = ['email', 'account_type', 'is_verified', 'is_staff', 'is_active', 'is_superuser']
    list_filter = ['username', 'email', 'account_type', 'date_joined']
    radio_fields = {'account_type': admin.VERTICAL}
    list_display_links = ['username']
    search_fields = ['username']
    ordering = ['username']
    fieldsets = [
        [
            'Basic Informations:', {
            'fields': [
                'username',
                'email',
                'password',
            ]
        }
        ],
        [
            'Joining Date:', {
            'fields': [
                'date_joined',
            ]
        }
        ],
        [
            'Profile Image:', {
            'fields': [
                'image',
            ]
        }
        ],
        [
            'Verification:', {
            'fields': [
                'is_verified',
            ]
        }
        ],
        [
            'Permissions:', {
            'fields': [
                'is_active',
                'is_staff',
                'is_superuser',
            ]
        }
        ]
    ]

    @admin.display(description='Permissions')
    def get_user_permissions(self, obj):
        return '\n'.join([p.user_permissions for p in obj.user_permissions.all()])


@admin.register(OneTimePassword)
class AdminOneTimePassword(admin.ModelAdmin):
    list_display = ['user', 'password', 'created_at', 'expires_in']
    fieldsets = [
        [
            'Basic Informations', {
            'fields': [
                'user',
                'password',
            ]
        }
        ],
        [
            'Dates', {
            'fields': [
                'created_at',
                'expires_in',
            ]
        }
        ]
    ]


@admin.register(Individual)
class AdminPrivateProfile(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'gender', 'country', 'province', 'city',
                    'street', 'postal_code', 'phone_number', 'website_url', 'facebook_url', 'instagram_url',
                    'linkedin_url']
    list_editable = ['first_name', 'last_name', 'gender', 'country', 'province', 'city',
                     'street', 'postal_code', 'phone_number', 'website_url', 'facebook_url', 'instagram_url',
                     'linkedin_url']
    list_filter = ['last_name', 'country', 'province', 'city', 'street', 'postal_code']
    list_display_links = ['user']
    search_fields = ['user']
    ordering = ['user']
    radio_fields = {'gender': admin.VERTICAL}
    fieldsets = [
        [
            'Basic Informations', {
            'fields': [
                'user',
                'first_name',
                'last_name',
                'gender',
            ]
        }
        ],
        [
            'Contact Informations', {
            'fields': [
                'phone_number',
            ]
        }
        ],
        [
            'Localization Informations', {
            'fields': [
                'country',
                'province',
                'city',
                'street',
                'postal_code',
            ]
        }
        ],
        [
            'Social Media Informations', {
            'fields': [
                'website_url',
                'facebook_url',
                'instagram_url',
                'linkedin_url',
            ]
        }
        ]
    ]


@admin.register(Business)
class AdminCompanyProfile(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'company_id', 'country', 'province', 'city',
                    'street', 'postal_code', 'phone_number', 'website_url', 'facebook_url', 'instagram_url',
                    'linkedin_url']
    list_editable = ['company_name', 'company_id', 'country', 'province', 'city',
                     'street', 'postal_code', 'phone_number', 'website_url', 'facebook_url', 'instagram_url',
                     'linkedin_url']
    list_filter = ['company_name', 'country', 'province', 'city', 'street', 'postal_code']
    list_display_links = ['user']
    search_fields = ['user']
    ordering = ['user']
    fieldsets = [
        [
            'Basic Informations', {
            'fields': [
                'user',
                'company_id',
                'company_name',
            ]
        }
        ],
        [
            'Contact Informations', {
            'fields': [
                'phone_number',
            ]
        }
        ],
        [
            'Localization Informations', {
            'fields': [
                'country',
                'province',
                'city',
                'street',
                'postal_code',
            ]
        }
        ],
        [
            'Social Media Informations', {
            'fields': [
                'website_url',
                'facebook_url',
                'instagram_url',
                'linkedin_url',
            ]
        }
        ]
    ]
