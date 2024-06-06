from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import User
from django.shortcuts import reverse
from django.core.validators import FileExtensionValidator
from PIL import Image
from uuid import uuid4


class ListingStatusManager(models.Manager):
    def get_by_name(self):
        return self.order_by("name")


class ListingStatus(models.Model):
    """
    Creating ListingStatus model instance.
    """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    objects = ListingStatusManager()

    class Meta:
        verbose_name = "Listing Status"
        verbose_name_plural = "Listing Statuses"

    def __str__(self) -> str:
        """
        Returns the string representation of the status name and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.name


class Category(models.Model):
    """
    Creating Category model instance.
    """

    id = models.AutoField(primary_key=True, editable=False)
    image = models.ImageField(upload_to="property_categories_images", null=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        """
        Returns the string representation of the category name and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.name

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL for a given category.

        Returns
        ----------
            str
        """
        return reverse(
            viewname="property-categories",
            kwargs={
                "category_slug": self.slug,
            },
        )


class Amenities(models.Model):
    """
    Creating Amenities model instance.
    """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    image = models.FileField(
        upload_to="icons/properties",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["svg"])],
    )

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"

    def __str__(self) -> str:
        """
        Returns the string representation of the amenity name and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.name


class Education(models.Model):
    """
    Creating Education model instance.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    distance = models.FloatField()
    rate = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations"

    def __str__(self) -> str:
        """
        Returns the string representation of the education institution name and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.name


class Shopping(models.Model):
    """
    Creating Shopping model instance.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    distance = models.FloatField()
    rate = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Shopping"

    def __str__(self) -> str:
        """
        Returns the string representation of the shopping places name and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.name


class HealthAndMedical(models.Model):
    """
    Creating HealthAndMedical model instance.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    distance = models.FloatField()
    rate = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Health & Medical"
        verbose_name_plural = "Health & Medicals"

    def __str__(self) -> str:
        """
        Returns the string representation of the health and medical institution name
        and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.name


class Transportation(models.Model):
    """
    Creating Transportation model instance.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    distance = models.FloatField()
    rate = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Transportation"
        verbose_name_plural = "Transportations"

    def __str__(self) -> str:
        """
        Returns the string representation of the transportation name and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.name


class City(models.Model):
    """
    Creating City model instance.
    """

    id = models.AutoField(primary_key=True)
    image = models.ImageField(
        upload_to="property_cities_images",
        null=True,
        blank=True,
        default="default_city_image.jpg",
    )
    name = models.CharField(default="", max_length=100, blank=True)
    slug = models.SlugField(max_length=100, null=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self) -> str:
        """
        Returns the string representation of the city name and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.name

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL for a given city.

        Returns
        ----------
            str
        """
        return reverse(
            viewname="property-cities",
            kwargs={
                "city_slug": self.slug,
            },
        )

    @property
    def rename_image(self) -> str:
        """
        Returns new name of uploaded user profile image.

        Returns:
        ----------
            str
        """
        return f"{uuid4()}" + f".{self.image.path.split(sep='.')[-1]}"


class Img(models.Model):
    """
    Creating Image model instance.
    """

    id = models.AutoField(primary_key=True)
    image = models.ImageField(
        upload_to="property_details_images", null=True, blank=True
    )

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self) -> str:
        """
        Returns the string representation of the image and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.image.name

    def save(self, *args, **kwargs):
        """
        Converts the article's image to a smaller size based on proportions.

        Parameters
        ----------
            args: tuple
            kwargs: dict

        Returns
        ----------
            None
        """
        super(Img, self).save(*args, **kwargs)

        img = Image.open(fp=self.image.path)

        if img.mode == "RGBA":
            img.convert(mode="RGB")

        img_width = img.width
        img_height = img.height

        output_width = 1100
        output_height = img_height * output_width / img_width

        img.thumbnail(size=(output_width, output_height))
        img.save(fp=self.image.path)

    @property
    def rename_image(self) -> str:
        """
        Returns new name of uploaded user profile image.

        Returns:
        ----------
            str
        """
        return f"{uuid4()}" + f".{self.image.path.split(sep='.')[-1]}"


class PropertyManager(models.Manager):
    def get_by_keyword(self, keyword, order_by):
        return self.filter(title__icontains=keyword).order_by(order_by)

    def get_by_filters(self, *order_by, **filters):
        return self.filter(**filters).order_by(*order_by)


class Property(models.Model):
    """
    Creating Property model instance.
    """

    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="properties"
    )
    title = models.CharField(max_length=100, unique=True)
    date_posted = models.DateTimeField(auto_now_add=True, editable=False)
    thumbnail = models.ImageField(upload_to="property_images", null=True)
    images = models.ManyToManyField(to=Img, related_name="images", blank=True)
    year_of_built = models.IntegerField()
    price = models.FloatField(default=1, null=True)
    number_of_bedrooms = models.IntegerField()
    number_of_bathrooms = models.IntegerField()
    square_meters = models.FloatField()
    parking_space = models.IntegerField()
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    city = models.ForeignKey(
        default="",
        to=City,
        on_delete=models.CASCADE,
        related_name="cities",
        null=True,
        blank=True,
    )
    province = models.CharField(default="", max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5, null=True)
    latitude = models.FloatField(max_length=20, null=True, blank=True)
    longitude = models.FloatField(max_length=20, null=True, blank=True)
    description = RichTextUploadingField(max_length=10000, unique=True)
    video = models.FileField(upload_to="property_videos")
    is_featured = models.BooleanField(default=False)
    favourites = models.ManyToManyField(to=User, related_name="favourites", blank=True)
    slug = models.SlugField(max_length=300, unique=True, null=True)
    listing_status = models.ForeignKey(
        to=ListingStatus, on_delete=models.CASCADE, related_name="listing_statuses"
    )
    category = models.ForeignKey(
        to=Category, related_name="categories", null=True, on_delete=models.CASCADE
    )
    amenities = models.ManyToManyField(to=Amenities, related_name="amenities")
    education = models.ManyToManyField(
        to=Education, related_name="education", blank=True
    )
    health_and_medical = models.ManyToManyField(
        to=HealthAndMedical, related_name="health_and_medical", blank=True
    )
    transportation = models.ManyToManyField(
        to=Transportation, related_name="transportation", blank=True
    )
    shopping = models.ManyToManyField(to=Shopping, related_name="shopping", blank=True)
    purchasing_user = models.ForeignKey(
        to=User, blank=True, null=True, on_delete=models.CASCADE
    )

    objects = PropertyManager()

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ["date_posted"]

    def __str__(self) -> str:
        """
        Returns the string representation of the property title and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.title

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL for a given property.

        Returns
        ----------
            str
        """
        return reverse(
            viewname="property-details",
            kwargs={
                "category_slug": self.category.slug,
                "property_slug": self.slug,
            },
        )

    def save(self, *args, **kwargs):
        """
        Converts the article's image to a smaller size based on proportions.

        Parameters
        ----------
            args: tuple
            kwargs: dict

        Returns
        ----------
            None
        """
        super(Property, self).save(*args, **kwargs)

        img = Image.open(fp=self.thumbnail.path)

        if img.mode == "RGBA":
            img.convert(mode="RGB")

        img_width = img.width
        img_height = img.height

        output_width = 1100
        output_height = img_height * output_width / img_width

        img.thumbnail(size=(output_width, output_height))
        img.save(fp=self.thumbnail.path)

    @property
    def rename_image(self) -> str:
        """
        Returns new name of uploaded user profile image.

        Returns:
        ----------
            str
        """
        return f"{uuid4()}" + f".{self.image.path.split(sep='.')[-1]}"


class TourSchedule(models.Model):
    """
    Creating TourSchedule model instance.
    """

    id = models.AutoField(primary_key=True, editable=False)
    customer = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=True, related_name="tour_schedules"
    )
    property = models.ForeignKey(to=Property, on_delete=models.CASCADE, null=True)
    date_sent = models.DateTimeField(auto_now=True, editable=False)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    message = models.TextField(max_length=10000)

    class Meta:
        verbose_name = "Tour Schedule"
        verbose_name_plural = "Tour Schedules"

    def __str__(self) -> str:
        """
        Returns the string representation of the username that sends a request to visit a property
        and displays it in the administrator panel.

        Returns
        ----------
            str
        """
        return self.name


class Review(models.Model):
    """
    Creating Reviews model instance.
    """

    id = models.AutoField(primary_key=True, editable=False)
    date_posted = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    property = models.ForeignKey(to=Property, on_delete=models.CASCADE, null=True)
    rate = models.IntegerField()
    content = models.TextField(max_length=20000)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self) -> str:
        """
        Returns the string representation of the reviews for the property and displays them in the administrator panel.

        Returns
        ----------
            str
        """
        return f"Reviewed by {self.user}"
