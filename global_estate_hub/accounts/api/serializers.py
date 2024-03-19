from rest_framework import serializers
from accounts.models import User, Individual, Business


class UserSerializer(serializers.Serializer):
    """
    User Model Serializer.
    """
    id = serializers.ReadOnlyField()
    username = serializers.CharField()
    email = serializers.EmailField()
    # image = serializers.ImageField()
    account_type = serializers.CharField()
    is_verified = serializers.BooleanField()
    is_active = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_agent = serializers.BooleanField()
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User


class IndividualProfileSerializer(serializers.Serializer):
    """
    Individual Model Serializer.
    """
    id = serializers.ReadOnlyField()
    user = UserSerializer()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    gender = serializers.CharField()
    country = serializers.CharField()
    province = serializers.CharField()
    city = serializers.CharField()
    street = serializers.CharField()
    postal_code = serializers.CharField()
    website_url = serializers.URLField()
    facebook_url = serializers.URLField()
    instagram_url = serializers.URLField()
    linkedin_url = serializers.URLField()

    class Meta:
        model = Individual


class BusinessProfileSerializer(serializers.Serializer):
    """
    Business Model Serializer
    """
    id = serializers.ReadOnlyField()
    user = UserSerializer()
    company_name = serializers.CharField()
    company_id = serializers.IntegerField()
    phone_number = serializers.CharField()
    country = serializers.CharField()
    province = serializers.CharField()
    city = serializers.CharField()
    street = serializers.CharField()
    postal_code = serializers.CharField()
    website_url = serializers.URLField()
    facebook_url = serializers.URLField()
    instagram_url = serializers.URLField()
    linkedin_url = serializers.URLField()

    class Meta:
        model = Business
