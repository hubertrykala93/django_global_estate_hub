from rest_framework import serializers
from properties.models import (
    ListingStatus,
    Category,
    Amenities,
    Education,
    Shopping,
    HealthAndMedical,
    Transportation,
    City,
    Property,
    TourSchedule,
    Review,
)
from accounts.api.serializers import UserUsernameSerializer


class ListingStatusSerializer(serializers.ModelSerializer):
    """
    ListingStatus Model Serializer.
    """

    class Meta:
        model = ListingStatus
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    Category Model Serializer.
    """

    class Meta:
        model = Category
        exclude = ["image"]


class AmenitiesSerializer(serializers.ModelSerializer):
    """
    Amenities Model Serializer.
    """

    class Meta:
        model = Amenities
        exclude = ["image"]


class EducationSerializer(serializers.ModelSerializer):
    """
    Education Model Serializer.
    """

    class Meta:
        model = Education
        fields = "__all__"


class ShoppingSerializer(serializers.ModelSerializer):
    """
    Shopping Model Serializer.
    """

    class Meta:
        model = Shopping
        fields = "__all__"


class HealthAndMedicalSerializer(serializers.ModelSerializer):
    """
    HealthAndMedical Model Serializer.
    """

    class Meta:
        model = HealthAndMedical
        fields = "__all__"


class TransportationSerializer(serializers.ModelSerializer):
    """
    Transportation Model Serializer.
    """

    class Meta:
        model = Transportation
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    """
    City Model Serializer.
    """

    class Meta:
        model = City
        exclude = ["image"]


class PropertySerializer(serializers.ModelSerializer):
    """
    Property Model Serializer.
    """

    date_posted = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    user = UserUsernameSerializer()
    city = CitySerializer()
    listing_status = ListingStatusSerializer()
    category = CategorySerializer()
    amenities = AmenitiesSerializer(many=True)
    education = EducationSerializer(many=True)
    health_and_medical = HealthAndMedicalSerializer(many=True)
    transportation = TransportationSerializer(many=True)
    shopping = ShoppingSerializer(many=True)

    class Meta:
        model = Property
        exclude = ["purchasing_user", "thumbnail", "images", "video"]


class PropertyTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ["id", "title"]


class TourScheduleSerializer(serializers.ModelSerializer):
    """
    TourSchedule Model Serializer.
    """

    customer = UserUsernameSerializer()
    property = PropertyTitleSerializer()
    date_sent = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = TourSchedule
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """
    Review Model Serializer.
    """

    date_posted = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    user = UserUsernameSerializer()
    property = PropertyTitleSerializer()

    class Meta:
        model = Review
        fields = "__all__"
