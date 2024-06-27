from rest_framework import serializers
from accounts.models import User, Individual, Business


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    account_type = serializers.ChoiceField(
        choices=(
            ("Individual", "Individual"),
            ("Business", "Business"),
        )
    )
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = User
        fields = [
            "id",
            "date_joined",
            "username",
            "email",
            "account_type",
            "image",
            "is_verified",
            "is_agent",
            "last_login",
        ]


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
