from django.contrib import admin
from .models import ListingStatus, Category, Amenities, Plan, TourSchedule, OfferContact, \
    Review, Education, HealthAndMedical, Transportation, Shopping, City, Property
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
    list_display_links = ['id']
    prepopulated_fields = {
        'slug': ['name'],
    }
    search_fields = ['name']
    ordering = ['id']
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


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    """
    Admin options and functionalities for Category model.
    """
    list_display = ['id', 'name', 'slug']
    list_editable = ['slug']
    list_filter = ['name']
    list_display_links = ['id']
    prepopulated_fields = {
        'slug': ['name'],
    }
    search_fields = ['name']
    ordering = ['id']
    fieldsets = [
        [
            'Category Name:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'Category Alias', {
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
    list_display_links = ['id']
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
    list_display_links = ['id']
    ordering = ['id']
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


@admin.register(Education)
class AdminEducation(admin.ModelAdmin):
    """
    Admin options and functionalities for Education model.
    """
    list_display = ['id', 'name', 'distance', 'rate']
    list_editable = ['name', 'distance', 'rate']
    list_display_links = ['id']
    search_fields = ['name']
    ordering = ['id']
    fieldsets = [
        [
            'Institution Name:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'Institution Distance', {
            'fields': [
                'distance',
            ]
        }
        ],
        [
            'Institution Rate:', {
            'fields': [
                'rate',
            ]
        }
        ]
    ]


@admin.register(HealthAndMedical)
class AdminHealthAndMedical(admin.ModelAdmin):
    """
    Admin options and functionalities for HealthAndMedical model.
    """
    list_display = ['id', 'name', 'distance', 'rate']
    list_editable = ['name', 'distance', 'rate']
    list_display_links = ['id']
    search_fields = ['name']
    ordering = ['id']
    fieldsets = [
        [
            'Institution Name:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'Institution Distance', {
            'fields': [
                'distance',
            ]
        }
        ],
        [
            'Institution Rate:', {
            'fields': [
                'rate',
            ]
        }
        ]
    ]


@admin.register(Transportation)
class AdminTransportation(admin.ModelAdmin):
    """
    Admin options and functionalities for Transportation model.
    """
    list_display = ['id', 'name', 'distance', 'rate']
    list_editable = ['name', 'distance', 'rate']
    list_display_links = ['id']
    search_fields = ['name']
    ordering = ['id']
    fieldsets = [
        [
            'Transportation Name:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'Transportation Distance', {
            'fields': [
                'distance',
            ]
        }
        ],
        [
            'Transportation Rate:', {
            'fields': [
                'rate',
            ]
        }
        ]
    ]


@admin.register(Shopping)
class AdminShopping(admin.ModelAdmin):
    """
    Admin options and functionalities for Shopping model.
    """
    """
    Admin options and functionalities for Transportation model.
    """
    list_display = ['id', 'name', 'distance', 'rate']
    list_editable = ['name', 'distance', 'rate']
    list_display_links = ['id']
    search_fields = ['name']
    ordering = ['id']
    fieldsets = [
        [
            'Shop Name:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'Shop Distance', {
            'fields': [
                'distance',
            ]
        }
        ],
        [
            'Shop Rate:', {
            'fields': [
                'rate',
            ]
        }
        ]
    ]


@admin.register(City)
class AdminCity(admin.ModelAdmin):
    """
    Admin options and functionalities for City model.
    """
    list_display = ['id', 'name', 'slug']
    list_filter = ['name']
    list_editable = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']
    ordering = ['id']
    fieldsets = [
        [
            'City Name:', {
            'fields': [
                'name',
            ]
        }
        ],
        [
            'City Alias:', {
            'fields': [
                'slug',
            ]
        }
        ]
    ]


@admin.register(Property)
class AdminProperty(admin.ModelAdmin):
    """
    Admin options and functionalities for Property model.
    """
    list_display = ['id', 'category', 'listing_status', 'number_of_bedrooms', 'number_of_bathrooms', 'user', 'city', 'date_posted', 'main_image',
                    'postal_code',
                    'province',
                    'country',
                    'country_code', 'latitude', 'longitude', 'video', 'is_featured', 'get_favourites',
                    'image_files',
                    'year_of_built', 'title', 'price', 'square_meters',
                    'parking_space', 'get_amenities', 'get_plans', 'get_educations',
                    'get_health_and_medicals', 'get_transportations', 'get_shops']
    list_filter = ['user', 'category', 'listing_status', 'number_of_bedrooms', 'number_of_bathrooms',
                   'year_of_built', 'city', 'province',
                   'country', 'is_featured', 'date_posted']
    list_editable = ['main_image', 'image_files', 'title', 'price', 'year_of_built', 'number_of_bedrooms',
                     'number_of_bathrooms',
                     'square_meters', 'parking_space', 'category', 'city', 'province', 'country', 'country_code',
                     'latitude',
                     'longitude', 'video',
                     'is_featured',
                     'listing_status']
    list_display_links = ['id']
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['user__username', 'title']
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
                'favourites',
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
            'Property Category:', {
            'fields': [
                'category',
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
            'Property Nearby:', {
            'fields': [
                'education',
                'health_and_medical',
                'transportation',
                'shopping',
            ]
        }
        ]
    ]

    @admin.display(description='Property Favourites')
    def get_favourites(self, obj):
        """
        Display in the admin panel all users who have added this property to their favorites.

        return: str
        """
        return '\n'.join([user.username for user in obj.favourites.all()])

    @admin.display(description='Property Plans')
    def get_plans(self, obj):
        """
        Displays in the admin panel all property plans assigned to a given property.

        return: str
        """
        return '\n'.join([p.name for p in obj.plan.all()])

    @admin.display(description='Amenities')
    def get_amenities(self, obj):
        """
        Displays in the admin panel all amenities assigned to a given property.

        return: str
        """
        return '\n'.join([a.name for a in obj.amenities.all()])

    @admin.display(description='Educations')
    def get_educations(self, obj):
        """
        Displays in the admin panel all education institutions assigned to a given property.

        return: str
        """
        return '\n'.join([e.name for e in obj.education.all()])

    @admin.display(description='Health & Medicals')
    def get_health_and_medicals(self, obj):
        """
        Displays in the admin panel all health and medicals institutions assigned to a given property.

        return: str
        """
        return '\n'.join([h.name for h in obj.health_and_medical.all()])

    @admin.display(description='Transportations')
    def get_transportations(self, obj):
        """
        Displays in the admin panel all transportations assigned to a given property.

        return: str
        """
        return '\n'.join([t.name for t in obj.transportation.all()])

    @admin.display(description='Shops')
    def get_shops(self, obj):
        """
        Displays in the admin panel all shops assigned to a given property.

        return: str
        """
        return '\n'.join([s.name for s in obj.shopping.all()])

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
    search_fields = ['to__username', 'name', 'email']
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
    search_fields = ['property__title', 'email']
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
    search_fields = ['user__username', 'property__title', 'full_name']
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
