from rest_framework import serializers
from accounts.models import User, Individual, Business
import re
import magic


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(method_name="get_image_name", allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "date_joined",
            "username",
            "email",
            "image",
            "account_type",
            "is_verified",
            "is_agent",
            "last_login",
        ]
        extra_kwargs = {
            "date_joined": {
                "format": "%Y-%m-%d %H:%M:%S",
                "read_only": True,
            },
            "last_login": {
                "format": "%Y-%m-%d %H:%M:%S",
                "read_only": True,
            }
        }

    def get_image_name(self, obj):
        return obj.image.name.split("/")[-1]


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, help_text="Enter the username.", allow_blank=True)
    email = serializers.CharField(max_length=100, help_text="Enter the e-mail address.", allow_blank=True)
    password = serializers.CharField(max_length=100, help_text="Enter the password", allow_blank=True, style={
        "input_type": "password",
    }, write_only=True)
    image = serializers.ImageField(help_text="Upload your image.", allow_null=True)
    account_type = serializers.ChoiceField(
        choices=(
            ("Individual", "Individual"),
            ("Business", "Business"),
        ),
        help_text="Select the account type.",
        allow_blank=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "image",
            "account_type",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)
        representation["image"] = instance.image.name.split("/")[-1]

        return representation

    def validate_username(self, username):
        if username == "":
            raise serializers.ValidationError(detail="Username is required.")

        if username and len(username) < 8:
            raise serializers.ValidationError(
                detail="The username should contain at least 8 characters."
            )

        if (
                username
                and len(username) >= 8
                and User.objects.filter(username=username).exists()
        ):
            raise serializers.ValidationError(detail="The user already exists.")

        return username

    def validate_email(self, email):
        if email == "":
            raise serializers.ValidationError(
                detail="E-mail address is required."
            )

        if email and not re.match(
                pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", string=email
        ):
            raise serializers.ValidationError(
                detail="The e-mail address format is invalid."
            )

        if (
                email
                and re.match(
            pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
            string=email,
        )
                and User.objects.filter(email=email).exists()
        ):
            raise serializers.ValidationError(
                detail="A user with this email address already exists."
            )

        return email

    def validate_password(self, password):
        if password == "":
            raise serializers.ValidationError(
                detail="Password is required."
            )

        if password and len(password) < 8:
            raise serializers.ValidationError(
                detail="The password should contain at least 8 characters."
            )

        if (
                password
                and len(password) >= 8
                and not re.match(
            pattern="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",
            string=password,
        )
        ):
            raise serializers.ValidationError(
                detail="The password should be at least 8 characters long, including at least one uppercase letter,"
                       " one lowercase letter, one digit, and one special character."
            )

        return password

    def validate_image(self, image):
        if image is None:
            raise serializers.ValidationError(detail="Image is required.")
        else:
            extension = image.name.split(".")[-1]
            allowed_extensions = ["jpg", "jpeg", "png", "svg", "webp"]

            if extension not in allowed_extensions:
                raise serializers.ValidationError(
                    detail="Invalid file format. Allowed formats are 'jpg', 'jpeg', 'png', 'svg', 'webp'.")

        return image

    def validate_account_type(self, account_type):
        if account_type == "":
            raise serializers.ValidationError(detail="Account type is required.")

        return account_type

    def create(self, validated_data):
        raw_password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(raw_password=raw_password)
        user.is_verified = True
        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100, help_text="Enter the username.", required=False
    )
    email = serializers.CharField(
        max_length=100, help_text="Enter the email address.", required=False
    )
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={
            "input_type": "password",
        },
        help_text="Enter the password.",
    )
    image = serializers.ImageField(help_text="Upload your photo.", required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "image",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance=instance)
        representation["image"] = instance.image.name.split("/")[-1]

        return representation

    def validate_username(self, username):
        if username and len(username) < 8:
            raise serializers.ValidationError(
                detail="The username should contain at least 8 characters."
            )

        if (
                self.instance.username != username
                and User.objects.filter(username=username).exists()
        ):
            raise serializers.ValidationError(detail="The user already exists.")

        return username

    def validate_email(self, email):
        if email and not re.match(
                pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", string=email
        ):
            raise serializers.ValidationError(
                detail="The e-mail address format is invalid."
            )

        if self.instance.email != email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail="A user with this e-mail address already exists."
            )

        return email

    def validate_password(self, password):
        if password and len(password) < 8:
            raise serializers.ValidationError(
                detail="The password should contain at least 8 characters."
            )

        if (
                password
                and len(password) >= 8
                and not re.match(
            pattern="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",
            string=password,
        )
        ):
            raise serializers.ValidationError(
                detail="The password should be at least 8 characters long, including at least one uppercase letter,"
                       " one lowercase letter, one digit, and one special character."
            )

        return password

    def validate_image(self, image):
        extension = image.name.split(".")[-1]
        allowed_extensions = ["jpg", "jpeg", "png", "svg", "webp"]

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                detail="Invalid file format. Allowed formats are 'jpg', 'jpeg', 'png', 'svg', 'webp'.")

        return image

    def update(self, instance, validated_data):
        if "password" in validated_data:
            raw_password = validated_data.pop("password")
            instance.set_password(raw_password=raw_password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class IndividualProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="id", read_only=True, required=False)
    first_name = serializers.CharField(
        max_length=100, help_text="Enter your first name.",
        required=False
    )
    last_name = serializers.CharField(max_length=100, help_text="Enter your last name.", required=False)
    phone_number = serializers.CharField(
        max_length=100, help_text="Enter your phone number.",
        required=False
    )
    gender = serializers.ChoiceField(
        choices=(("Male", "Male"), ("Female", "Female")),
        help_text="Select your gender.",
        required=False
    )
    country = serializers.CharField(
        max_length=100, help_text="Enter your country of residence.", required=False
    )
    province = serializers.CharField(
        max_length=100, help_text="Enter your province of residence.", required=False
    )
    city = serializers.CharField(
        max_length=100, help_text="Enter your city of residence.", required=False
    )
    street = serializers.CharField(
        max_length=100, help_text="Enter your street address.", required=False
    )
    postal_code = serializers.CharField(
        max_length=100, help_text="Enter your postal code.", required=False
    )
    website_url = serializers.URLField(
        label="Website URL",
        max_length=150,
        help_text="Copy the URL of your website. The URL should start with 'http://'.",
        required=False
    )
    facebook_url = serializers.URLField(
        label="Facebook URL",
        max_length=150,
        help_text="Copy the URL of your Facebook profile. The URL should start with 'http://'.",
        required=False
    )
    instagram_url = serializers.URLField(
        label="Instagram URL",
        max_length=150,
        help_text="Copy the URL of your Instagram profile. The URL should start with 'http://'.",
        required=False
    )
    linkedin_url = serializers.URLField(
        label="LinkedIn URL",
        max_length=150,
        help_text="Copy the URL of your LinkedIn profile. The URL should start with 'http://'.",
        required=False
    )

    class Meta:
        model = Individual
        fields = "__all__"


class BusinessProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="id", read_only=True, required=False)
    company_name = serializers.CharField(max_length=100, help_text="Enter your company name.", required=False)
    company_id = serializers.IntegerField(max_value=100, help_text="Enter your company ID", required=False)
    phone_number = serializers.CharField(
        max_length=100, help_text="Enter your phone number.",
        required=False
    )
    country = serializers.CharField(
        max_length=100, help_text="Enter your country of residence.", required=False
    )
    province = serializers.CharField(
        max_length=100, help_text="Enter your province of residence.", required=False
    )
    city = serializers.CharField(
        max_length=100, help_text="Enter your city of residence.", required=False
    )
    street = serializers.CharField(
        max_length=100, help_text="Enter your street address.", required=False
    )
    postal_code = serializers.CharField(
        max_length=100, help_text="Enter your postal code.", required=False
    )
    website_url = serializers.URLField(
        label="Website URL",
        max_length=150,
        help_text="Copy the URL of your website. The URL should start with 'http://'.",
        required=False
    )
    facebook_url = serializers.URLField(
        label="Facebook URL",
        max_length=150,
        help_text="Copy the URL of your Facebook profile. The URL should start with 'http://'.",
        required=False
    )
    instagram_url = serializers.URLField(
        label="Instagram URL",
        max_length=150,
        help_text="Copy the URL of your Instagram profile. The URL should start with 'http://'.",
        required=False
    )
    linkedin_url = serializers.URLField(
        label="LinkedIn URL",
        max_length=150,
        help_text="Copy the URL of your LinkedIn profile. The URL should start with 'http://'.",
        required=False
    )

    class Meta:
        model = Business
        fields = "__all__"
