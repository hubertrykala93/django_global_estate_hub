from rest_framework import serializers
from properties.models import ListingStatus, Category, Amenities, Education, Shopping, HealthAndMedical, Transportation, \
    City, Property
from accounts.api.serializers import UserSerializer


class ListingStatusSerializer(serializers.Serializer):
    """
    ListingStatus Model Serializer.
    """
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    slug = serializers.SlugField()

    class Meta:
        model = ListingStatus


class CategorySerializer(serializers.Serializer):
    """
    Category Model Serializer.
    """
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    slug = serializers.SlugField()

    class Meta:
        model = Category


class AmenitiesSerializer(serializers.Serializer):
    """
    Amenities Model Serializer.
    """
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    slug = serializers.CharField()

    class Meta:
        model = Amenities


class EducationSerializer(serializers.Serializer):
    """
    Education Model Serializer.
    """
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    distance = serializers.FloatField()
    rate = serializers.FloatField()

    class Meta:
        model = Education


class ShoppingSerializer(serializers.Serializer):
    """
    Shopping Model Serializer.
    """
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    distance = serializers.FloatField()
    rate = serializers.FloatField()

    class Meta:
        model = Shopping


class HealthAndMedicalSerializer(serializers.Serializer):
    """
    HealthAndMedical Model Serializer.
    """
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    distance = serializers.FloatField()
    rate = serializers.FloatField()

    class Meta:
        model = HealthAndMedical


class TransportationSerializer(serializers.Serializer):
    """
    Transportation Model Serializer.
    """
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    distance = serializers.FloatField()
    rate = serializers.FloatField()

    class Meta:
        model = Transportation


class CitySerializer(serializers.Serializer):
    """
    City Model Serializer.
    """
    id = serializers.ReadOnlyField()
    name = serializers.CharField()
    slug = serializers.SlugField()

    class Meta:
        model = City


class PropertySerializer(serializers.Serializer):
    """
    Property Model Serializer.
    """
    id = serializers.ReadOnlyField()
    user = UserSerializer()
    title = serializers.CharField()
    date_posted = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    thumbnail = serializers.ImageField()
    year_of_built = serializers.IntegerField()
    price = serializers.FloatField()
    number_of_bedrooms = serializers.IntegerField()
    number_of_bathrooms = serializers.IntegerField()
    square_meters = serializers.FloatField()
    parking_space = serializers.IntegerField()
    postal_code = serializers.CharField()
    city = CitySerializer()
    province = serializers.CharField()
    country = serializers.CharField()
    country_code = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    is_featured = serializers.BooleanField()
    favourites = UserSerializer(read_only=True, many=True)
    slug = serializers.SlugField()
    listing_status = ListingStatusSerializer()
    category = CategorySerializer()
    amenities = AmenitiesSerializer(read_only=True, many=True)
    education = EducationSerializer(read_only=True, many=True)
    health_and_medical = HealthAndMedicalSerializer(read_only=True, many=True)
    transportation = TransportationSerializer(read_only=True, many=True)
    shopping = ShoppingSerializer(read_only=True, many=True)
    quantity_of_purchases = serializers.IntegerField()
    purchasing_user = UserSerializer()

    class Meta:
        model = Property
