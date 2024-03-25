from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Individual, Business
from django.contrib.sessions.models import Session
import pprint
from django.utils.translation import ngettext
from django.contrib import messages

admin.site.unregister(Group)


@admin.register(Session)
class AdminSession(admin.ModelAdmin):
    """
    Admin options and functionalities for Session model.
    """
    list_display = ['get_user', 'session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    ordering = ['-expire_date']

    @admin.display(description='user')
    def get_user(self, obj) -> str:
        """
        Displays in the admin panel all users assigned to a given session.

        Parameters
        ----------
            obj: django.contrib.session.models.Session

        Returns
        ----------
            str
        """
        session_user = obj.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=session_user)
        return user.username

    def _session_data(self, obj) -> str:
        """
        Displays in the admin panel session data assigned to a given user.

        Parameters
        ----------
            obj: django.contrib.session.models.Session

        Returns
        ----------
            str
        """
        return pprint.pformat(obj.get_decoded()).replace('\n', '\n')

    _session_data.allow_tags = True


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    """
    Admin options and functionalities for User model.
    """
    list_display = ['id', 'username', 'email', 'image', 'password', 'account_type', 'is_verified', 'is_staff',
                    'is_active', 'is_superuser', 'date_joined', 'last_login', 'is_agent']
    list_editable = ['email', 'account_type', 'is_verified', 'is_staff', 'is_active', 'is_superuser', 'is_agent']
    list_filter = ['username', 'email', 'account_type', 'date_joined', 'is_agent']
    radio_fields = {'account_type': admin.VERTICAL}
    list_display_links = ['id']
    search_fields = ['username']
    ordering = ['date_joined']
    actions = ['make_verified']
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
        ],
        [
            'Additionals', {
            'fields': [
                'is_agent',
            ]
        }
        ]
    ]

    @admin.action(description='Make all selected Users verified')
    def make_verified(self, request, queryset) -> None:
        """
        Highlights all selected users that have the 'is_verified' attribute set to 'False'.

        Parameters
        ----------
            request: django.core.handlers.wsgi.WSGIRequest
            queryset: django.db.models.query.Queryset

        Returns
        ----------
            None
        """
        updated = queryset.update(is_verified=True)

        self.message_user(request=request,
                          message=ngettext(singular=f'{updated} user has been verified successfully.',
                                           plural=f'{updated} users have been verified successfully.',
                                           number=updated),
                          level=messages.SUCCESS)


@admin.register(Individual)
class AdminIndividualProfile(admin.ModelAdmin):
    """
    Admin options and functionalities for Individual model.
    """
    list_display = ['id', 'user', 'first_name', 'last_name', 'gender', 'country', 'province', 'city',
                    'street', 'postal_code', 'phone_number', 'website_url', 'facebook_url', 'instagram_url',
                    'linkedin_url']
    list_editable = ['first_name', 'last_name', 'gender', 'country', 'province', 'city',
                     'street', 'postal_code', 'phone_number', 'website_url', 'facebook_url', 'instagram_url',
                     'linkedin_url']
    list_filter = ['last_name', 'country', 'province', 'city', 'street', 'postal_code']
    list_display_links = ['id']
    search_fields = ['user__username']
    ordering = ['id']
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
class AdminBusinessProfile(admin.ModelAdmin):
    """
    Admin options and functionalities for Business model.
    """
    list_display = ['id', 'user', 'company_name', 'company_id', 'country', 'province', 'city',
                    'street', 'postal_code', 'phone_number', 'website_url', 'facebook_url', 'instagram_url',
                    'linkedin_url']
    list_editable = ['company_name', 'company_id', 'country', 'province', 'city',
                     'street', 'postal_code', 'phone_number', 'website_url', 'facebook_url', 'instagram_url',
                     'linkedin_url']
    list_filter = ['company_name', 'country', 'province', 'city', 'street', 'postal_code']
    list_display_links = ['id']
    search_fields = ['user__username']
    ordering = ['id']
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
