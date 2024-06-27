from rest_framework import serializers
from core.models import Newsletter


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Newsletter Model Serializer.
    """
    subscribed_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Newsletter
        fields = '__all__'
