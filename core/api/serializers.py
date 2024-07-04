from rest_framework import serializers
from core.models import Newsletter
import re


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Newsletter Model Serializer.
    """

    subscribed_at = serializers.DateTimeField(
        read_only=True, format="%Y-%m-%d %H:%M:%S"
    )
    email = serializers.CharField(max_length=100, help_text="Enter the e-mail address.", allow_blank=True)

    class Meta:
        model = Newsletter
        fields = "__all__"

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

        if email and Newsletter.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail="The e-mail address already exists."
            )

        return email
