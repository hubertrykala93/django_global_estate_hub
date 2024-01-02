from django.contrib import admin
from .models import ListingStatus, PropertyType, Amenities, Property
from django.utils.translation import ngettext
from django.contrib import messages


@admin.register(ListingStatus)
class AdminListingStatus(admin.ModelAdmin):
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


@admin.register(Property)
class AdminProperty(admin.ModelAdmin):
    list_display = ['id', 'user', 'date_posted', 'image', 'title', 'year_of_built', 'price', 'number_of_bedrooms',
                    'number_of_bathrooms', 'square_meters', 'parking_space', 'city', 'province', 'country', 'video',
                    'featured', 'favourite', 'slug', 'listing_status', 'get_property_types',
                    'get_amenities']
    list_filter = ['user', 'date_posted', 'title', 'year_of_built', 'price', 'number_of_bedrooms',
                   'number_of_bathrooms', 'square_meters', 'parking_space', 'city', 'province', 'country', 'featured',
                   'favourite', 'listing_status']
    list_editable = ['image', 'title', 'year_of_built', 'price', 'number_of_bedrooms', 'number_of_bathrooms',
                     'square_meters', 'parking_space', 'city', 'province', 'country', 'video', 'featured', 'favourite',
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
            'Base Informations:', {
            'fields': [
                'title',
                'year_of_built',
                'price',
                'number_of_bedrooms',
                'number_of_bathrooms',
                'square_meters',
                'parking_space',
            ]
        }
        ],
        [
            'Localization:', {
            'fields': [
                'city',
                'province',
                'country',
            ]
        }
        ],
        [
            'Video Presentation:', {
            'fields': [
                'video',
            ]
        }
        ],
        [
            'Status:', {
            'fields': [
                'featured',
                'favourite',
            ]
        }
        ],
        [
            'Alias', {
            'fields': [
                'slug',
            ]
        }
        ],
        [
            'Additionals:', {
            'fields': [
                'listing_status',
                'property_type',
                'amenities',
            ]
        }
        ]
    ]

    @admin.display(description='Property Types')
    def get_property_types(self, obj):
        return '\n'.join([t.name for t in obj.property_type.all()])

    @admin.display(description='Amenities')
    def get_amenities(self, obj):
        return '\n'.join([a.name for a in obj.amenities.all()])

    @admin.action(description='Highlight selected Properties')
    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)

        self.message_user(request=request,
                          message=ngettext(singular=f'{updated} property has been featured successfully.',
                                           plural=f'{updated} properties have been featured successfully.',
                                           number=updated),
                          level=messages.SUCCESS)

    @admin.action(description='Remove highlights from selected properties.')
    def remove_featured(self, request, queryset):
        updated = queryset.update(featured=False)

        self.message_user(request=request,
                          message=ngettext(singular=f'{updated} highlight has been successfully removed.',
                                           plural=f'{updated} highlights have been successfully removed.',
                                           number=updated),
                          level=messages.SUCCESS)
