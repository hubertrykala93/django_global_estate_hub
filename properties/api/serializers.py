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
    Review,
    Img,
)
from accounts.models import User
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView


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


class PropertySerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField(method_name="get_thumbnail_name")
    images = serializers.SerializerMethodField(method_name="get_images_names")
    video = serializers.SerializerMethodField(method_name="get_video_name")
    amenities = AmenitiesSerializer(many=True)
    education = EducationSerializer(many=True)
    health_and_medical = HealthAndMedicalSerializer(many=True)
    transportation = TransportationSerializer(many=True)
    shopping = ShoppingSerializer(many=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "date_posted",
            "user",
            "title",
            "description",
            "slug",
            "listing_status",
            "category",
            "thumbnail",
            "images",
            "video",
            "year_of_built",
            "price",
            "number_of_bedrooms",
            "number_of_bathrooms",
            "square_meters",
            "parking_space",
            "country",
            "country_code",
            "province",
            "city",
            "postal_code",
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
        extra_kwargs = {
            "date_posted": {
                "format": "%Y-%m-%d %H:%M:%S",
            }
        }

    def get_thumbnail_name(self, obj):
        return obj.thumbnail.name.split("/")[-1]

    def get_images_names(self, obj):
        return [img.image.name.split("/")[-1] for img in obj.images.all()]

    def get_video_name(self, obj):
        return obj.video.name.split("/")[-1]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        extra_kwargs = {
            "date_posted": {
                "format": "%Y-%m-%d %H:%M:%S",
                "read_only": True,
            }
        }


class ReviewCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.none(),
        allow_null=False,
        required=False,
    )
    property = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(),
        allow_null=False,
        required=False
    )
    content = serializers.CharField(
        max_length=10000,
        required=False,
        allow_blank=True,
    )
    rate = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.context.get("request").user

        if self.context.get("request").user.is_staff:
            self.fields["user"].queryset = User.objects.all()

        else:
            self.fields["user"].queryset = User.objects.filter(username=user)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "property",
            "content",
            "rate",
            "active",
        ]
        extra_kwargs = {
            "active": {
                "read_only": True,
            },
        }

    def validate_content(self, content):
        if content == "":
            raise serializers.ValidationError(
                detail="Content is required.",
            )

        if len(content) < 10:
            raise serializers.ValidationError(
                detail="The review should be at least 10 characters long.",
            )

        return content

    def validate_rate(self, rate):
        if rate is None:
            raise serializers.ValidationError(
                detail="Rate is required."
            )

        if rate < 1 or rate > 5:
            raise serializers.ValidationError(
                detail="Rate should be between 1 and 5, inclusive.",
            )

        return rate

    def create(self, validated_data):
        if self.context.get("request"):
            if self.context.get("request").user.is_staff:
                validated_data["active"] = True

            else:
                validated_data["active"] = False

        return super().create(validated_data=validated_data)
