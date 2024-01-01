from django.db import models
from accounts.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class ListingStatus(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Listing Status'
        verbose_name_plural = 'Listing Statuses'

    def __str__(self):
        return self.name


class PropertyType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Property Type'
        verbose_name_plural = 'Property Types'

    def __str__(self):
        return self.name


class Amenities(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'

    def __str__(self):
        return self.name


class Property(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='users')
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='property_images')
    title = models.CharField(max_length=100)
    year_of_built = models.IntegerField()
    price = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    number_of_bathrooms = models.IntegerField()
    square_meters = models.FloatField()
    parking_space = models.IntegerField()
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = RichTextUploadingField(max_length=10000, unique=True)
    video = models.FileField(upload_to='property_videos')
    featured = models.BooleanField(default=False)
    favourite = models.BooleanField(default=False)
    slug = models.SlugField(max_length=300, unique=True, null=True)
    listing_status = models.ForeignKey(to=ListingStatus, on_delete=models.CASCADE, related_name='listing_statuses')
    property_type = models.ManyToManyField(to=PropertyType, related_name='property_types')
    amenities = models.ManyToManyField(to=Amenities, related_name='amenities')

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['date_posted']

    def __str__(self):
        return self.title
