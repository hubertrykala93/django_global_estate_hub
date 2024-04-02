from rest_framework import serializers
from accounts.models import User, Individual, Business


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'email', 'image', 'account_type', 'is_verified', 'is_agent',
                  'last_login']


class UserUsernameSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField()

    class Meta:
        model = User


class IndividualProfileSerializer(serializers.ModelSerializer):
    """
    Individual Model Serializer.
    """
    user = UserSerializer()

    class Meta:
        model = Individual
        fields = '__all__'


class BusinessProfileSerializer(serializers.Serializer):
    """
    Business Model Serializer
    """
    user = UserSerializer()

    class Meta:
        model = Business
        fields = '__all__'
