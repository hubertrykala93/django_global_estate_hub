from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import User


class ListingStatus(models.Model):
    """
    Creating ListingStatus model instance.
    """
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Listing Status'
        verbose_name_plural = 'Listing Statuses'

    def __str__(self):
        """
        Returns the string representation of the status name and displays it in the administrator panel.

        return: str
        """
        return self.name


class PropertyType(models.Model):
    """
    Creating PropertyType model instance.
    """
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Property Type'
        verbose_name_plural = 'Property Types'

    def __str__(self):
        """
        Returns the string representation of the property type name and displays it in the administrator panel.

        return: str
        """
        return self.name


class Amenities(models.Model):
    """
    Creating Amenities model instance.
    """
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'

    def __str__(self):
        """
        Returns the string representation of the amenity name and displays it in the administrator panel.

        return: str
        """
        return self.name


class Plan(models.Model):
    """
    Creating Plan model instance.
    """
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=f'property_images/plans/{name}')
    floor_square_meters = models.FloatField()
    number_of_bedrooms = models.IntegerField()
    number_of_bathrooms = models.IntegerField()

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'

    def __str__(self):
        """
        Returns the string representation of the plan name and displays it in the administrator panel.

        return: str
        """
        return self.name


class NearbyObject(models.Model):
    """
    Creating NearbyCategory model instance.
    """
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    distance = models.FloatField(max_length=8)
    rate = models.IntegerField()

    class Meta:
        verbose_name = 'Nearby Object'
        verbose_name_plural = 'Nearby Objects'

    def __str__(self):
        """
        Returns the string representation of the nearby object name and displays it in the administrator panel.

        return: str
        """
        return self.name


class Nearby(models.Model):
    """
    Creating Nearby model instance.
    """
    id = models.AutoField(primary_key=True, editable=False)
    category = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='icons/properties')
    nearby_objects = models.ManyToManyField(to=NearbyObject, related_name='nearby_objects')

    class Meta:
        verbose_name = 'Nearby'
        verbose_name_plural = 'Nearby'

    def __str__(self):
        """
        Returns the string representation of the object located near the property
        and displays it in the administrator panel.

        return: str
        """
        return self.name


class Property(models.Model):
    """
    Creating Property model instance.
    """
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='users')
    title = models.CharField(max_length=100, unique=True)
    date_posted = models.DateTimeField(auto_now_add=True, editable=False)
    main_image = models.ImageField(upload_to='property_images', null=True)
    image_files = models.FileField(upload_to=f'property_images/{title}', null=True, blank=True)
    year_of_built = models.IntegerField()
    price = models.CharField(max_length=20)
    number_of_bedrooms = models.IntegerField()
    number_of_bathrooms = models.IntegerField()
    square_meters = models.FloatField()
    parking_space = models.IntegerField()
    postal_code = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5, null=True)
    latitude = models.FloatField(max_length=20, null=True)
    longitude = models.FloatField(max_length=20, null=True)
    description = RichTextUploadingField(max_length=10000, unique=True)
    video = models.FileField(upload_to='property_videos')
    is_featured = models.BooleanField(default=False)
    favourites = models.ManyToManyField(to=User, related_name='favourites', blank=True)
    slug = models.SlugField(max_length=300, unique=True, null=True)
    listing_status = models.ForeignKey(to=ListingStatus, on_delete=models.CASCADE, related_name='listing_statuses')
    property_type = models.ManyToManyField(to=PropertyType, related_name='property_types')
    amenities = models.ManyToManyField(to=Amenities, related_name='amenities')
    plan = models.ManyToManyField(to=Plan, related_name='property_plan', blank=True)
    nearby = models.ForeignKey(to=Nearby, on_delete=models.CASCADE, null=True, related_name='nearby', blank=True)

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['date_posted']

    def __str__(self):
        """
        Returns the string representation of the property title and displays it in the administrator panel.

        return: str
        """
        return self.title


class TourSchedule(models.Model):
    """
    Creating TourSchedule model instance.
    """
    id = models.AutoField(primary_key=True, editable=False)
    to = models.ForeignKey(to=User, on_delete=models.CASCADE)
    property = models.ForeignKey(to=Property, on_delete=models.CASCADE, null=True)
    date_sent = models.DateTimeField(auto_now=True, editable=False)
    date = models.DateTimeField()
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=10000)

    class Meta:
        verbose_name = 'Tour Schedule'
        verbose_name_plural = 'Tour Schedules'

    def __str__(self):
        """
        Returns the string representation of the username that sends a request to visit a property
        and displays it in the administrator panel.

        return: str
        """
        return self.name


class OfferContact(models.Model):
    """
    Creating OfferContact model instance.
    """
    id = models.AutoField(primary_key=True, editable=False)
    date_sent = models.DateTimeField(auto_now=True, editable=False)
    property = models.ForeignKey(to=Property, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    message = models.TextField(max_length=20000, null=True)

    class Meta:
        verbose_name = 'Offer Contact'
        verbose_name_plural = 'Offer Contacts'

    def __str__(self):
        """
        Returns the string representation of the username that sends a contact request
        and displays it in the administrator panel.

        return: str
        """
        return f'{self.first_name}' + ' ' + f'{self.last_name}'


class Review(models.Model):
    """
    Creating Reviews model instance.
    """
    id = models.AutoField(primary_key=True, editable=False)
    date_posted = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    property = models.ForeignKey(to=Property, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100, null=True)
    rate = models.IntegerField()
    content = models.TextField(max_length=20000)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        """
        Returns the string representation of the reviews for the property and displays them in the administrator panel.

        return: str
        """
        return f'Reviewed by {self.user}'
