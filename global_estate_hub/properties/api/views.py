from rest_framework.generics import ListAPIView
from properties.models import Property
from .serializers import PropertySerializer
from .permissions import AdminOnly
from django_filters.rest_framework import DjangoFilterBackend


class PropertyList(ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['listing_status', 'category', 'city']
    # permission_classes = [AdminOnly]
