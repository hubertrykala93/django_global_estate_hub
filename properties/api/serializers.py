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
    Img,
)
from accounts.models import User


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


class ImgSerializer(serializers.ModelSerializer):
    """
    Img Model Serializer.
    """

    class Meta:
        model = Img
        fields = "__all__"


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

    date_posted = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    thumbnail = serializers.SerializerMethodField(method_name="get_thumbnail_name")
    video = serializers.SerializerMethodField(method_name="get_video_name")
    images = serializers.SerializerMethodField(method_name="get_images_names")
    user = serializers.SlugRelatedField(slug_field="id", queryset=User.objects.all())
    description = serializers.SerializerMethodField(method_name="get_description")
    city = serializers.SlugRelatedField(slug_field="name", queryset=City.objects.all())
    listing_status = serializers.SlugRelatedField(
        slug_field="name", queryset=ListingStatus.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )
    amenities = serializers.SlugRelatedField(
        slug_field="name", queryset=Amenities.objects.all(), many=True
    )
    # amenities = AmenitiesSerializer(many=True)
    education = EducationSerializer(many=True)
    health_and_medical = HealthAndMedicalSerializer(many=True)
    transportation = TransportationSerializer(many=True)
    shopping = ShoppingSerializer(many=True)
    favourites = serializers.SlugRelatedField(
        slug_field="username", many=True, queryset=User.objects.all()
    )
    purchasing_user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Property
        fields = [
            "id",
            "date_posted",
            "user",
            "title",
            "slug",
            "thumbnail",
            "video",
            "images",
            "listing_status",
            "category",
            "year_of_built",
            "price",
            "description",
            "number_of_bedrooms",
            "number_of_bathrooms",
            "square_meters",
            "parking_space",
            "country",
            "country_code",
            "province",
            "city",
            "latitude",
            "longitude",
            "amenities",
            "education",
            "health_and_medical",
            "transportation",
            "shopping",
            "is_featured",
            "favourites",
            "purchasing_user",
        ]

    def get_thumbnail_name(self, obj):
        return obj.thumbnail.name.split("/")[-1]

    def get_video_name(self, obj):
        return obj.video.name.split("/")[-1]

    def get_images_names(self, obj):
        return [img.image.name.split("/")[-1] for img in obj.images.all()]

    def get_description(self, obj):
        return obj.description.replace("<p>", "").replace("</p>", "")


class TourScheduleSerializer(serializers.ModelSerializer):
    """
    TourSchedule Model Serializer.
    """

    customer = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        help_text="Select the customer.",
        required=False,
    )
    property = serializers.SlugRelatedField(
        slug_field="title",
        queryset=Property.objects.all(),
        required=False,
        help_text="Select the property title",
    )
    date_sent = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    date = serializers.CharField(
        max_length=20,
        help_text="Enter the meeting date. The meeting date must be in the format 'DD.MM.YYYY'.",
        required=False,
    )
    time = serializers.CharField(
        max_length=20,
        help_text="Enter the meeting time or write 'Any' if any time works for you. The meeting time must be in the format 'HH:MM'.",
        required=False,
    )
    name = serializers.CharField(
        label="Full Name", required=False, help_text="Enter your full name."
    )
    phone_number = serializers.CharField(
        required=False, help_text="Enter your phone number."
    )
    message = serializers.CharField(
        max_length=10000, required=False, help_text="Write a message to the seller."
    )

    class Meta:
        model = TourSchedule
        fields = "__all__"

    def validate_date(self, d):
        from datetime import date
        import datetime

        if d is None:
            raise serializers.ValidationError(detail="The date field cannot be empty.")

        day = d.split(".")[0]
        month = d.split(".")[1]
        year = d.split(".")[2]

        if day[0] == "0":
            day = day[1]

        if month[0] == "0":
            month = month[1]

        converted_date = date(year=int(year), month=int(month), day=int(day))
        now = datetime.datetime.now()
        now_date = datetime.date(now.year, now.month, now.day)

        if converted_date < now_date:
            raise serializers.ValidationError(
                detail="You cannot schedule an appointment in the past."
            )

        if converted_date == now_date:
            raise serializers.ValidationError(
                detail="You cannot schedule an appointment for the same day, please choose at least one day ahead."
            )

        return converted_date

    def validate_time(self, time):
        if time is None:
            raise serializers.ValidationError(detail="The time field cannot be empty.")

        return time

    def validate_name(self, name):
        if name is None:
            raise serializers.ValidationError(
                detail="The full name field cannot be empty."
            )

        return name

    def validate_phone_number(self, phone_number):
        if phone_number is None:
            raise serializers.ValidationError(
                detail="The phone number field cannot be empty."
            )

        return phone_number

    def validate_message(self, message):
        if message is None:
            raise serializers.ValidationError(
                detail="The message field cannot be empty."
            )

        return message


class ReviewSerializer(serializers.ModelSerializer):
    """
    Review Model Serializer.
    """

    date_posted = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    user = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        help_text="Select the review author.",
        required=False,
    )
    property = serializers.SlugRelatedField(
        slug_field="title",
        queryset=Property.objects.all(),
        help_text="Select the property.",
        required=False,
    )
    rate = serializers.IntegerField(help_text="Rate the property.", required=False)
    content = serializers.CharField(
        help_text="Write your review.", required=False, max_length=10000
    )

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["active"]

    def create(self, validated_data):
        review = Review(**validated_data)
        review.active = True
        review.save()

        return review

    def validate_rate(self, rate):
        if rate is None:
            raise serializers.ValidationError(detail="The rate field cannot be empty.")

        if rate and rate < 1:
            raise serializers.ValidationError(
                detail="The rating cannot be less than 1."
            )

        if rate and rate > 5:
            raise serializers.ValidationError(
                detail="The rating cannot be more than 5."
            )

        return rate

    def validate_content(self, content):
        if content is None:
            raise serializers.ValidationError(
                detail="The content field cannot be empty."
            )

        if content and len(content) < 5:
            raise serializers.ValidationError(
                detail="The content of the review must be at least 5 characters long."
            )

        return content
