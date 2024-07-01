from rest_framework import serializers
from accounts.models import User, Individual, Business
import re


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    username = serializers.CharField(max_length=100, help_text="Type your username.")
    email = serializers.EmailField(max_length=100, help_text="Type your e-mail address.")
    password = serializers.CharField(
        write_only=True,
        required=False,
        style={
            "input_type": "password",
        },
        help_text="Type your password."
    )
    account_type = serializers.ChoiceField(
        choices=(
            ("Individual", "Individual"),
            ("Business", "Business"),
        ),
        help_text="Choose your account type."
    )
    image = serializers.ImageField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    is_agent = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "date_joined",
            "username",
            "email",
            "password",
            "account_type",
            "image",
            "is_verified",
            "is_agent",
            "last_login",
        ]

    def validate_username(self, username):
        if username is None:
            raise serializers.ValidationError(
                detail="The username field cannot be empty."
            )

        if username and len(username) < 8:
            raise serializers.ValidationError(detail="The username should contain at least 8 characters.")

        if username and len(username) >= 8 and User.objects.filter(username=username).exists():
            raise serializers.ValidationError(detail="The user already exists.")

        return username

    def validate_email(self, email):
        if email is None:
            raise serializers.ValidationError(detail="The e-mail field cannot be empty.")

        if email and not re.match(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", string=email):
            raise serializers.ValidationError(detail="The e-mail address format is invalid.")

        if email and re.match(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                              string=email) and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(detail="A user with this email address already exists.")

        return email

    def validate_password(self, password):
        if password is None:
            raise serializers.ValidationError(detail="The password field cannot be empty.")

        if password and len(password) < 8:
            raise serializers.ValidationError(
                detail="The password should contain at least 8 characters.")

        if password and len(password) >= 8 and not re.match(
                pattern="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", string=password):
            raise serializers.ValidationError(
                detail="The password should be at least 8 characters long, including at least one uppercase letter,"
                       " one lowercase letter, one digit, and one special character.")

        return password

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(raw_password=password)
        user.is_verified = True
        user.save()

        return user

    def update(self, instance, validated_data):
        if validated_data.get("password"):
            password = validated_data.pop("password")

            instance.set_password(raw_password=password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class UserUsernameSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField()

    class Meta:
        model = User


class IndividualProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Individual
        fields = "__all__"


class BusinessProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Business
        fields = "__all__"
