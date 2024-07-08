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
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from datetime import datetime
from datetime import timedelta


class ListingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingStatus
        fields = "__all__"


class ListingStatusCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = ListingStatus
        fields = "__all__"
        extra_kwargs = {
            "slug": {
                "read_only": True
            }
        }

    def validate_name(self, name):
        if name == "":
            raise serializers.ValidationError(detail="Name is required.")

        if isinstance(self.context["view"], CreateAPIView):
            if name and ListingStatus.objects.filter(name=name).exists():
                raise serializers.ValidationError(detail="A listing status with this name already exists.")

        else:
            if self.instance.name != name and ListingStatus.objects.filter(name=name).exists():
                raise serializers.ValidationError(detail="A listing status with this name already exists.")

        return name


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(method_name="get_image_name")

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "image",
        ]

    def get_image_name(self, obj):
        return obj.image.name.split("/")[-1]


class CategoryCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True)
    name = serializers.CharField(allow_blank=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "image",
        ]
        extra_kwargs = {
            "slug": {
                "read_only": True,
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(self.context["view"], RetrieveUpdateAPIView):
            self.fields["image"].allow_null = False
            self.fields["image"].required = False

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)

        representation["image"] = instance.image.name.split("/")[-1]

        return representation

    def validate_image(self, image):
        extension = image.name.split(".")[-1]
        allowed_extensions = ["jpg", "jpeg", "png", "svg", "webp"]

        if isinstance(self.context["view"], CreateAPIView):
            if image is None:
                raise serializers.ValidationError(detail="Image is required.")

            if extension not in allowed_extensions:
                raise serializers.ValidationError(
                    detail="Invalid file format. Allowed formats are 'jpg', 'jpeg', 'png', 'svg', 'webp'.")

        if isinstance(self.context["view"], RetrieveUpdateAPIView):
            if image is not None:
                if extension not in allowed_extensions:
                    raise serializers.ValidationError(
                        detail="Invalid file format. Allowed formats are 'jpg', 'jpeg', 'png', 'svg', 'webp'.")

        return image

    def validate_name(self, name):
        if name == "":
            raise serializers.ValidationError(detail="Name is required.")

        return name


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = "__all__"


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        exclude = ["image"]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class ShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping
        fields = "__all__"


class HealthAndMedicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthAndMedical
        fields = "__all__"


class TransportationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transportation
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ["image"]


class PropertySerializer(serializers.ModelSerializer):
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
    class Meta:
        model = TourSchedule
        fields = [
            "id",
            "date_sent",
            "property",
            "customer",
            "name",
            "date",
            "time",
            "phone_number",
            "message",
        ]
        extra_kwargs = {
            "date_sent": {
                "format": "%Y-%m-%d %H:%M:%S",
                "read_only": True,
            }
        }


class TourScheduleCreateSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all())

    class Meta:
        model = TourSchedule
        fields = [
            "id",
            "date_sent",
            "property",
            "customer",
            "name",
            "date",
            "time",
            "phone_number",
            "message",
        ]
        extra_kwargs = {
            "name": {
                "allow_blank": True,
            },
            "date": {
                "allow_blank": True,
                "help_text": "The date must be in the format 'YYYY-MM-DD'.",
            },
            "time": {
                "allow_blank": True,
                "help_text": "The time must be in the format 'HH' or 'Any'.",
            },
            "phone_number": {
                "allow_blank": True,
            },
            "message": {
                "allow_blank": True,
            },
            "customer": {
                "read_only": True,
            }
        }

    def validate_name(self, name):
        if name == "":
            raise serializers.ValidationError(detail="Name is required.")

        return name

    def validate_date(self, date):
        if date == "":
            raise serializers.ValidationError(detail="Date is required.")

        if len(date.split("-")) != 3:
            raise serializers.ValidationError(detail="Invalid format. The correct date format is 'YYYY-MM-DD'.")

        else:
            splitted_date = date.split("-")
            date_datetime = datetime(year=int(splitted_date[0]), month=int(splitted_date[1]),
                                     day=int(splitted_date[2]))

            if date_datetime.strftime("%Y-%m-%d") < datetime.now().strftime("%Y-%m-%d"):
                raise serializers.ValidationError(
                    detail="Schedule the meeting at least one day ahead, up to five days ahead.")

            if date_datetime.strftime("%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d"):
                raise serializers.ValidationError(
                    detail="Schedule the meeting at least one day ahead, up to five days ahead.")

            if date_datetime > datetime.now() + timedelta(days=5):
                raise serializers.ValidationError(
                    detail="Schedule the meeting at least one day ahead, up to five days ahead.")

        return date

    def validate_time(self, time):
        if time == "":
            raise serializers.ValidationError(detail="Time is required.")

        return time

    def validate_phone_number(self, phone_number):
        if phone_number == "":
            raise serializers.ValidationError(detail="Phone number is required.")

        return phone_number

    def validate_message(self, message):
        if message == "":
            raise serializers.ValidationError(detail="Message is required.")

        return message


class ReviewSerializer(serializers.ModelSerializer):
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
