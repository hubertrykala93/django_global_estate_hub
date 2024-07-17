from rest_framework import serializers
from core.models import Newsletter
import re
from rest_framework.generics import CreateAPIView


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Newsletter Model Serializer.
    """

    class Meta:
        model = Newsletter
        fields = "__all__"
        extra_kwargs = {
            "subscribed_at": {
                "format": "%Y-%m-%d %H:%M:%S",
            }
        }


class NewsletterCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        max_length=200,
        allow_blank=True,
    )

    class Meta:
        model = Newsletter
        fields = "__all__"
        extra_kwargs = {
            "subscribed_at": {
                "format": "%Y-%m-%d %H:%M:%S",
            }
        }

    def validate_email(self, email):
        if email == "":
            raise serializers.ValidationError(detail="E-mail address is required.")

        if email and not re.match(
            pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", string=email
        ):
            raise serializers.ValidationError(
                detail="The e-mail address format is invalid."
            )

        if email and Newsletter.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail="The e-mail address already exists."
            )

        return email
