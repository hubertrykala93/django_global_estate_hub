from django.contrib import admin
from .models import ListingStatus, PropertyType, Amenities, Plan, NearbyObject, Nearby, TourSchedule, OfferContact, \
    Review, Property
from django.utils.translation import ngettext
from django.contrib import messages


@admin.register(ListingStatus)
class AdminListingStatus(admin.ModelAdmin):
    """
    Admin options and functionalities for ListingStatus model.
    """
    list_display = ['id', 'name', 'slug']
    list_editable = ['slug']
    list_filter = ['name']
    list_display_links = ['name']
    prepopulated_fields = {
        'slug': ['name'],
    }
    search_fields = ['name']
    ordering = ['name']
    fieldsets = [
        [
            'Listing Status Name:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'Listing Status Alias', {
            'fields': [
                'slug',
            ]
        }
        ]
    ]


@admin.register(PropertyType)
class AdminPropertyType(admin.ModelAdmin):
    """
    Admin options and functionalities for PropertyType model.
    """
    list_display = ['id', 'name', 'slug']
    list_editable = ['slug']
    list_filter = ['name']
    list_display_links = ['name']
    prepopulated_fields = {
        'slug': ['name'],
    }
    search_fields = ['name']
    ordering = ['name']
    fieldsets = [
        [
            'Property Type Name:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'Property Type Alias', {
            'fields': [
                'slug',
            ]
        }
        ]
    ]


@admin.register(Amenities)
class AdminAmenities(admin.ModelAdmin):
    """
    Admin options and functionalities for Amenities model.
    """
    list_display = ['id', 'name', 'slug']
    list_editable = ['slug']
    list_filter = ['name']
    list_display_links = ['name']
    prepopulated_fields = {
        'slug': ['name'],
    }
    search_fields = ['name']
    ordering = ['id']
    fieldsets = [
        [
            'Amenity Name:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'Amenity Alias', {
            'fields': [
                'slug',
            ]
        }
        ]
    ]


@admin.register(Plan)
class AdminPlan(admin.ModelAdmin):
    """
    Admin options and functionalities for Plan model.
    """
    list_display = ['id', 'name', 'image', 'floor_square_meters', 'number_of_bedrooms', 'number_of_bathrooms']
    list_editable = ['image', 'floor_square_meters', 'number_of_bedrooms', 'number_of_bathrooms']
    list_filter = ['name', 'floor_square_meters', 'number_of_bedrooms', 'number_of_bathrooms']
    list_display_links = ['name']
    fieldsets = [
        [
            'Basic Informations:', {
            'fields': [
                'name',
                'image',
            ]
        }
        ],
        [
            'Area Informations:', {
            'fields': [
                'floor_square_meters',
                'number_of_bedrooms',
                'number_of_bathrooms',
            ]
        }
        ]
    ]


@admin.register(NearbyObject)
class AdminNearbyObject(admin.ModelAdmin):
    """
    Admin options and functionalities for NearbyCategory model.
    """
    list_display = ['id', 'name', 'distance', 'rate']
    list_editable = ['name', 'distance', 'rate']
    list_filter = ['name', 'distance', 'rate']
    list_display_links = ['id']

    fieldsets = [
        [
            'Name:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'Distance:', {
            'fields': [
                'distance',
            ]
        }
        ],
        [
            'Rate:', {
            'fields': [
                'rate',
            ]
        }
        ]
    ]


@admin.register(Nearby)
class AdminNearby(admin.ModelAdmin):
    """
    Admin options and functionalities for Plan model.
    """
    list_display = ['id', 'name', 'icon', 'get_nearby_objects']
    list_editable = ['icon']
    list_filter = ['name']
    list_display_links = ['name']
    fieldsets = [
        [
            'Basic Informations:', {
            'fields': [
                'name',
                'icon',
                'nearby_objects',
            ]
        }
        ],
    ]

    @admin.display(description='Nearbies')
    def get_nearby_objects(self, obj):
        """
        Displays in the admin panel all nearby objects assigned to a given nearby.

        return: str
        """
        return '\n'.join([n.name for n in obj.nearby_objects.all()])


@admin.register(Property)
class AdminProperty(admin.ModelAdmin):
    """
    Admin options and functionalities for Property model.
    """
    list_display = ['id', 'user', 'title', 'date_posted', 'main_image', 'postal_code', 'province', 'country',
                    'country_code',
                    'latitude', 'longitude', 'video', 'is_featured', 'is_favourite', 'listing_status', 'image_files',
                    'year_of_built', 'price', 'number_of_bedrooms', 'number_of_bathrooms', 'square_meters',
                    'parking_space', 'city', 'get_property_types', 'get_amenities', 'get_plans', 'nearby']
    list_filter = ['user', 'date_posted', 'title', 'year_of_built', 'price', 'number_of_bedrooms',
                   'number_of_bathrooms', 'square_meters', 'parking_space', 'postal_code', 'city', 'province',
                   'country',
                   'country_code', 'latitude', 'longitude', 'is_featured',
                   'is_favourite', 'listing_status']
    list_editable = ['main_image', 'image_files', 'title', 'year_of_built', 'price', 'number_of_bedrooms',
                     'number_of_bathrooms',
                     'square_meters', 'parking_space', 'city', 'province', 'country', 'country_code', 'latitude',
                     'longitude', 'video',
                     'is_featured', 'is_favourite',
                     'listing_status']
    list_display_links = ['user']
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['user', 'title']
    ordering = ['date_posted']
    actions = ['make_featured', 'remove_featured']

    fieldsets = [
        [
            'Creator:', {
            'fields': [
                'user',
            ]
        }
        ],
        [
            'Basic Informations:', {
            'fields': [
                'title',
                'slug',
                'year_of_built',
                'main_image',
                'video',
                'price',
                'number_of_bedrooms',
                'number_of_bathrooms',
                'square_meters',
                'parking_space',
            ]
        }
        ],
        [
            'Description:', {
            'fields': [
                'description',
            ]
        }
        ],
        [
            'Localization:', {
            'fields': [
                'latitude',
                'longitude',
                'postal_code',
                'city',
                'province',
                'country',
                'country_code',
            ]
        }
        ],
        [
            'Uploadings:', {
            'fields': [
                'image_files',
            ]
        }
        ],
        [
            'Additionals:', {
            'fields': [
                'is_featured',
                'is_favourite',
            ]
        }
        ],
        [
            'Property Status:', {
            'fields': [
                'listing_status'
            ]
        }
        ],
        [
            'Property Type:', {
            'fields': [
                'property_type',
            ]
        }
        ],
        [
            'Property Amenities:', {
            'fields': [
                'amenities',
            ]
        }
        ],
        [
            'Property Plans:', {
            'fields': [
                'plan',
            ]
        }
        ],
        [
            'Nearbies:', {
            'fields': [
                'nearby',
            ]
        }
        ]
    ]

    @admin.display(description='Property Plans')
    def get_plans(self, obj):
        """
        Displays in the admin panel all property plans assigned to a given property.

        return: str
        """
        return '\n'.join([p.name for p in obj.plan.all()])

    @admin.display(description='Property Types')
    def get_property_types(self, obj):
        """
        Displays in the admin panel all property types assigned to a given property.

        return: str
        """
        return '\n'.join([t.name for t in obj.property_type.all()])

    @admin.display(description='Amenities')
    def get_amenities(self, obj):
        """
        Displays in the admin panel all amenities assigned to a given property.

        return: str
        """
        return '\n'.join([a.name for a in obj.amenities.all()])

    @admin.action(description='Highlight selected Properties')
    def make_featured(self, request, queryset):
        """
        Highlights all selected properties that have the 'is_featured' attribute set to 'False'.

        return: None
        """
        updated = queryset.update(featured=True)

        self.message_user(request=request,
                          message=ngettext(singular=f'{updated} property has been featured successfully.',
                                           plural=f'{updated} properties have been featured successfully.',
                                           number=updated),
                          level=messages.SUCCESS)

    @admin.action(description='Remove highlights from selected properties.')
    def remove_featured(self, request, queryset):
        """
        Unhighlights all selected properties that have the 'is_featured' attribute set to 'True'.

        return: None
        """
        updated = queryset.update(featured=False)

        self.message_user(request=request,
                          message=ngettext(singular=f'{updated} highlight has been successfully removed.',
                                           plural=f'{updated} highlights have been successfully removed.',
                                           number=updated),
                          level=messages.SUCCESS)


@admin.register(TourSchedule)
class AdminTourSchedule(admin.ModelAdmin):
    list_display = ['id', 'to', 'property', 'date_sent', 'date', 'name', 'email', 'message']
    list_editable = ['date', 'property', 'name', 'email']
    list_filter = ['to', 'date_sent', 'date', 'name', 'email']
    list_display_links = ['id']
    search_fields = ['to', 'name', 'email']
    ordering = ['date_sent']
    fieldsets = [
        [
            'From User:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'To User:', {
            'fields': [
                'to',
            ]
        }
        ],
        [
            'Related to:', {
            'fields': [
                'property',
            ]
        }
        ],
        [
            'Date:', {
            'fields': [
                'date',
            ]
        }
        ],
        [
            'Message Body:', {
            'fields': [
                'message',
            ]
        }
        ]
    ]


@admin.register(OfferContact)
class AdminOfferContact(admin.ModelAdmin):
    """
    Admin options and functionalities for OfferContact model.
    """
    list_display = ['id', 'date_sent', 'property', 'first_name', 'last_name', 'email', 'phone_number', 'message']
    list_filter = ['first_name', 'last_name', 'email']
    list_display_links = ['first_name']
    ordering = ['date_sent']
    fieldsets = [
        [
            'Request Informations:', {
            'fields': [
                'first_name',
                'last_name',
                'email',
                'phone_number',
            ]
        }
        ],
        [
            'Related to:', {
            'fields': [
                'property',
            ]
        }
        ],
        [
            'Message Body:', {
            'fields': [
                'message',
            ]
        }
        ]
    ]


@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    """
    Admin options and functionalities for Review model.
    """
    list_display = ['id', 'date_posted', 'user', 'property', 'full_name', 'rate', 'content', 'active']
    list_filter = ['user', 'date_posted', 'property', 'full_name', 'rate', 'active']
    list_editable = ['user', 'property', 'full_name', 'rate', 'active']
    list_display_links = ['id']
    search_fields = ['user', 'property', 'full_name']
    ordering = ['date_posted']
    actions = ['approve_reviews']
    fieldsets = [
        [
            'Creator:', {
            'fields': [
                'user',
                'full_name',
            ]
        }
        ],
        [
            'Related to:', {
            'fields': [
                'property',
            ]
        }
        ],
        [
            'Review Body:', {
            'fields': [
                'content',
            ]
        }
        ],
        [
            'Rating:', {
            'fields': [
                'rate',
            ]
        }
        ],
        [
            'Status:', {
            'fields': [
                'active',
            ]
        }
        ]
    ]

    @admin.action(description='Approve selected Reviews')
    def approve_reviews(self, request, queryset):
        """
        Approves all selected reviews that have the 'active' attribute set to 'False'.

        return: None
        """
        updated = queryset.update(active=True)

        self.message_user(request=request,
                          message=ngettext(singular=f'{updated} review has been approved successfully.',
                                           plural=f'{updated} reviews have been approved successfully.',
                                           number=updated),
                          level=messages.SUCCESS)
