from rest_framework import serializers
from core.models import Newsletter


class NewsletterSerializer(serializers.Serializer):
    """
    Newsletter Model Serializer.
    """
    id = serializers.ReadOnlyField()
    subscribed_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    email = serializers.EmailField()

    class Meta:
        model = Newsletter
