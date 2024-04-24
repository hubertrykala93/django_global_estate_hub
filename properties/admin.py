from django.contrib import admin
from .models import (
    ListingStatus,
    Category,
    Amenities,
    TourSchedule,
    Review,
    Education,
    HealthAndMedical,
    Transportation,
    Shopping,
    City,
    Property,
    Img,
)
from django.utils.translation import ngettext
from django.contrib import messages


@admin.register(ListingStatus)
class AdminListingStatus(admin.ModelAdmin):
    """
    Admin options and functionalities for ListingStatus model.
    """

    list_display = ["id", "name", "slug"]
    list_editable = ["name", "slug"]
    list_display_links = ["id"]
    prepopulated_fields = {
        "slug": ["name"],
    }
    search_fields = ["name"]
    ordering = ["id"]
    fieldsets = [
        [
            "Listing Status Name:",
            {
                "fields": [
                    "name",
                ]
            },
        ],
        [
            "Listing Status Alias",
            {
                "fields": [
                    "slug",
                ]
            },
        ],
    ]


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    """
    Admin options and functionalities for Category model.
    """

    list_display = ["id", "name", "slug", "image"]
    list_editable = ["name", "slug", "image"]
    list_display_links = ["id"]
    prepopulated_fields = {
        "slug": ["name"],
    }
    search_fields = ["name"]
    ordering = ["id"]
    fieldsets = [
        [
            "Category Name:",
            {
                "fields": [
                    "name",
                ]
            },
        ],
        [
            "Category Alias",
            {
                "fields": [
                    "slug",
                ]
            },
        ],
    ]


@admin.register(Amenities)
class AdminAmenities(admin.ModelAdmin):
    """
    Admin options and functionalities for Amenities model.
    """

    list_display = ["id", "name", "slug", "image"]
    list_editable = ["name", "slug", "image"]
    list_display_links = ["id"]
    prepopulated_fields = {
        "slug": ["name"],
    }
    search_fields = ["name"]
    ordering = ["id"]
    fieldsets = [
        [
            "Amenity Name:",
            {
                "fields": [
                    "name",
                ]
            },
        ],
        [
            "Uploadings:",
            {
                "fields": [
                    "image",
                ]
            },
        ],
        [
            "Amenity Alias",
            {
                "fields": [
                    "slug",
                ]
            },
        ],
    ]


@admin.register(Education)
class AdminEducation(admin.ModelAdmin):
    """
    Admin options and functionalities for Education model.
    """

    list_display = ["id", "name", "distance", "rate"]
    list_editable = ["name", "distance", "rate"]
    list_display_links = ["id"]
    search_fields = ["name"]
    ordering = ["id"]
    fieldsets = [
        [
            "Institution Name:",
            {
                "fields": [
                    "name",
                ]
            },
        ],
        [
            "Institution Distance",
            {
                "fields": [
                    "distance",
                ]
            },
        ],
        [
            "Institution Rate:",
            {
                "fields": [
                    "rate",
                ]
            },
        ],
    ]


@admin.register(HealthAndMedical)
class AdminHealthAndMedical(admin.ModelAdmin):
    """
    Admin options and functionalities for HealthAndMedical model.
    """

    list_display = ["id", "name", "distance", "rate"]
    list_editable = ["name", "distance", "rate"]
    list_display_links = ["id"]
    search_fields = ["name"]
    ordering = ["id"]
    fieldsets = [
        [
            "Institution Name:",
            {
                "fields": [
                    "name",
                ]
            },
        ],
        [
            "Institution Distance",
            {
                "fields": [
                    "distance",
                ]
            },
        ],
        [
            "Institution Rate:",
            {
                "fields": [
                    "rate",
                ]
            },
        ],
    ]


@admin.register(Transportation)
class AdminTransportation(admin.ModelAdmin):
    """
    Admin options and functionalities for Transportation model.
    """

    list_display = ["id", "name", "distance", "rate"]
    list_editable = ["name", "distance", "rate"]
    list_display_links = ["id"]
    search_fields = ["name"]
    ordering = ["id"]
    fieldsets = [
        [
            "Transportation Name:",
            {
                "fields": [
                    "name",
                ]
            },
        ],
        [
            "Transportation Distance",
            {
                "fields": [
                    "distance",
                ]
            },
        ],
        [
            "Transportation Rate:",
            {
                "fields": [
                    "rate",
                ]
            },
        ],
    ]


@admin.register(Shopping)
class AdminShopping(admin.ModelAdmin):
    """
    Admin options and functionalities for Shopping model.
    """

    """
    Admin options and functionalities for Transportation model.
    """
    list_display = ["id", "name", "distance", "rate"]
    list_editable = ["name", "distance", "rate"]
    list_display_links = ["id"]
    search_fields = ["name"]
    ordering = ["id"]
    fieldsets = [
        [
            "Shop Name:",
            {
                "fields": [
                    "name",
                ]
            },
        ],
        [
            "Shop Distance",
            {
                "fields": [
                    "distance",
                ]
            },
        ],
        [
            "Shop Rate:",
            {
                "fields": [
                    "rate",
                ]
            },
        ],
    ]


@admin.register(City)
class AdminCity(admin.ModelAdmin):
    """
    Admin options and functionalities for City model.
    """

    list_display = ["id", "name", "slug", "image"]
    list_editable = ["name", "slug", "image"]
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ["name"]
    ordering = ["-id"]
    fieldsets = [
        [
            "City Image:",
            {
                "fields": [
                    "image",
                ]
            },
        ],
        [
            "City Name:",
            {
                "fields": [
                    "name",
                ]
            },
        ],
        [
            "City Alias:",
            {
                "fields": [
                    "slug",
                ]
            },
        ],
    ]


@admin.register(Img)
class AdminImage(admin.ModelAdmin):
    """
    Admin options and functionalities for Img model.
    """

    list_display = ["id", "image"]
    list_editable = ["image"]
    ordering = ["id"]
    fieldsets = [
        [
            "Property Images:",
            {
                "fields": [
                    "image",
                ]
            },
        ]
    ]


@admin.register(Property)
class AdminProperty(admin.ModelAdmin):
    """
    Admin options and functionalities for Property model.
    """

    list_display = [
        "id",
        "date_posted",
        "user",
        "title",
        "slug",
        "year_of_built",
        "price",
        "number_of_bedrooms",
        "number_of_bathrooms",
        "square_meters",
        "parking_space",
        "latitude",
        "longitude",
        "country",
        "country_code",
        "province",
        "city",
        "postal_code",
        "thumbnail",
        "get_images",
        "video",
        "listing_status",
        "category",
        "get_favourites",
        "get_amenities",
        "get_educations",
        "get_health_and_medicals",
        "get_transportations",
        "get_shops",
        "is_featured",
        "purchasing_user",
    ]

    list_filter = [
        "user",
        "category",
        "listing_status",
        "number_of_bedrooms",
        "number_of_bathrooms",
        "year_of_built",
        "city",
        "province",
        "country",
        "is_featured",
        "date_posted",
    ]

    list_display_links = ["id"]
    prepopulated_fields = {"slug": ["title"]}
    search_fields = ["user__username", "title"]
    ordering = ["-id"]
    actions = ["make_featured", "remove_featured"]
    fieldsets = [
        [
            "Creator:",
            {
                "fields": [
                    "user",
                ]
            },
        ],
        [
            "Basic Informations:",
            {
                "fields": [
                    "title",
                    "slug",
                    "year_of_built",
                    "price",
                    "number_of_bedrooms",
                    "number_of_bathrooms",
                    "square_meters",
                    "parking_space",
                ]
            },
        ],
        [
            "Description:",
            {
                "fields": [
                    "description",
                ]
            },
        ],
        [
            "Localization:",
            {
                "fields": [
                    "latitude",
                    "longitude",
                    "postal_code",
                    "city",
                    "province",
                    "country",
                    "country_code",
                ]
            },
        ],
        [
            "Uploadings:",
            {
                "fields": [
                    "thumbnail",
                    "images",
                    "video",
                ]
            },
        ],
        [
            "Additionals:",
            {
                "fields": [
                    "is_featured",
                    "favourites",
                ]
            },
        ],
        ["Property Status:", {"fields": ["listing_status"]}],
        [
            "Property Category:",
            {
                "fields": [
                    "category",
                ]
            },
        ],
        [
            "Property Amenities:",
            {
                "fields": [
                    "amenities",
                ]
            },
        ],
        [
            "Property Nearby:",
            {
                "fields": [
                    "education",
                    "health_and_medical",
                    "transportation",
                    "shopping",
                ]
            },
        ],
    ]

    @admin.display(description="Property Images")
    def get_images(self, obj) -> str:
        """
        Display in the admin panel all users who have added this property to their favorites.

        Parameters
        ----------
            obj: properties.models.Property

        Returns
        ----------
            str
        """
        return "\n".join([str(img) for img in obj.images.all()])

    @admin.display(description="Property Favourites")
    def get_favourites(self, obj) -> str:
        """
        Display in the admin panel all users who have added this property to their favorites.

        Parameters
        ----------
            obj: properties.models.Property

        Returns
        ----------
            str
        """
        return "\n".join([user.username for user in obj.favourites.all()])

    @admin.display(description="Amenities")
    def get_amenities(self, obj) -> str:
        """
        Displays in the admin panel all amenities assigned to a given property.

        Parameters
        ----------
            obj: properties.models.Property

        Returns
        ----------
            str
        """
        return "\n".join([a.name for a in obj.amenities.all()])

    @admin.display(description="Educations")
    def get_educations(self, obj) -> str:
        """
        Displays in the admin panel all education institutions assigned to a given property.

        Parameters
        ----------
            obj: properties.models.Property

        Returns
        ----------
            str
        """
        return "\n".join([e.name for e in obj.education.all()])

    @admin.display(description="Health & Medicals")
    def get_health_and_medicals(self, obj) -> str:
        """
        Displays in the admin panel all health and medicals institutions assigned to a given property.

        Parameters
        ----------
            obj: properties.models.Property

        Returns
        ----------
            str
        """
        return "\n".join([h.name for h in obj.health_and_medical.all()])

    @admin.display(description="Transportations")
    def get_transportations(self, obj) -> str:
        """
        Displays in the admin panel all transportations assigned to a given property.

        Parameters
        ----------
            obj: properties.models.Property

        Returns
        ----------
            str
        """
        return "\n".join([t.name for t in obj.transportation.all()])

    @admin.display(description="Shops")
    def get_shops(self, obj) -> str:
        """
        Displays in the admin panel all shops assigned to a given property.

        Parameters
        ----------
            obj: properties.models.Property

        Returns
        ----------
            str
        """
        return "\n".join([s.name for s in obj.shopping.all()])

    @admin.action(description="Make all selected Properties featured")
    def make_featured(self, request, queryset) -> None:
        """
        Highlights all selected properties that have the 'is_featured' attribute set to 'False'.

        Parameters
        ----------
            request: django.core.handlers.wsgi.WSGIRequest
            queryset: django.db.models.query.Queryset

        Returns
        ----------
            None
        """
        updated = queryset.update(featured=True)

        self.message_user(
            request=request,
            message=ngettext(
                singular=f"{updated} property has been featured successfully.",
                plural=f"{updated} properties have been featured successfully.",
                number=updated,
            ),
            level=messages.SUCCESS,
        )

    @admin.action(description="Remove highlights featured from selected properties.")
    def remove_featured(self, request, queryset) -> None:
        """
        Unhighlights all selected properties that have the 'is_featured' attribute set to 'True'.

        Parameters
        ----------
            request: django.core.handlers.wsgi.WSGIRequest
            queryset: django.db.models.query.Queryset

        Returns
        ----------
            None
        """
        updated = queryset.update(featured=False)

        self.message_user(
            request=request,
            message=ngettext(
                singular=f"{updated} highlight has been successfully removed.",
                plural=f"{updated} highlights have been successfully removed.",
                number=updated,
            ),
            level=messages.SUCCESS,
        )


@admin.register(TourSchedule)
class AdminTourSchedule(admin.ModelAdmin):
    """
    Admin options and functionalities for TourSchedule model.
    """

    list_display = [
        "id",
        "customer",
        "property",
        "date_sent",
        "date",
        "time",
        "name",
        "phone_number",
        "message",
    ]
    list_filter = ["customer", "date_sent", "date", "time", "name", "phone_number"]
    list_display_links = ["id"]
    search_fields = ["customer__username", "name", "phone_number"]
    ordering = ["date_sent"]
    fieldsets = [
        [
            "From User:",
            {
                "fields": [
                    "name",
                ]
            },
        ],
        [
            "Customer:",
            {
                "fields": [
                    "customer",
                ]
            },
        ],
        [
            "Related to:",
            {
                "fields": [
                    "property",
                ]
            },
        ],
        [
            "Date and Time:",
            {
                "fields": [
                    "date",
                    "time",
                ]
            },
        ],
        [
            "Contact:",
            {
                "fields": [
                    "phone_number",
                ]
            },
        ],
        [
            "Message Body:",
            {
                "fields": [
                    "message",
                ]
            },
        ],
    ]


@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    """
    Admin options and functionalities for Review model.
    """

    list_display = [
        "id",
        "date_posted",
        "user",
        "property",
        "rate",
        "content",
        "active",
    ]
    list_filter = ["user__username", "date_posted", "property__title", "active"]
    list_editable = ["user", "property", "rate", "active"]
    list_display_links = ["id"]
    search_fields = ["user__username", "property__title", "full_name"]
    ordering = ["date_posted"]
    actions = ["approve_reviews"]
    fieldsets = [
        [
            "Creator:",
            {
                "fields": [
                    "user",
                ]
            },
        ],
        [
            "Related to:",
            {
                "fields": [
                    "property",
                ]
            },
        ],
        [
            "Review Body:",
            {
                "fields": [
                    "content",
                ]
            },
        ],
        [
            "Rating:",
            {
                "fields": [
                    "rate",
                ]
            },
        ],
        [
            "Status:",
            {
                "fields": [
                    "active",
                ]
            },
        ],
    ]

    @admin.action(description="Approve selected Reviews")
    def approve_reviews(self, request, queryset) -> None:
        """
        Approves all selected reviews that have the 'active' attribute set to 'False'.

        Parameters
        ----------
            request: django.core.handlers.wsgi.WSGIRequest
            queryset: django.db.models.query.Queryset

        Returns
        ----------
            None
        """
        updated = queryset.update(active=True)

        self.message_user(
            request=request,
            message=ngettext(
                singular=f"{updated} review has been approved successfully.",
                plural=f"{updated} reviews have been approved successfully.",
                number=updated,
            ),
            level=messages.SUCCESS,
        )
