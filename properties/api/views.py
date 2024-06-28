from rest_framework.generics import ListAPIView, RetrieveAPIView
from properties.models import Property, TourSchedule, Review
from .serializers import PropertySerializer, TourScheduleSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend


class PropertyAPIView(ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "user": ["exact"],
        "user__username": ["exact"],
        "year_of_built": ["lte", "gte", "exact", "lt", "gt"],
        "price": ["lte", "gte", "exact", "lt", "gt"],
        "number_of_bedrooms": ["lte", "gte", "exact", "lt", "gt"],
        "number_of_bathrooms": ["lte", "gte", "exact", "lt", "gt"],
        "square_meters": ["lte", "gte", "exact", "lt", "gt"],
        "city": ["exact"],
        "city__name": ["exact"],
        "province": ["exact"],
        "country": ["exact"],
        "is_featured": ["exact"],
        "listing_status": ["exact"],
        "listing_status__name": ["exact"],
        "category": ["exact"],
        "category__name": ["exact"],
    }

    def get_view_name(self) -> str:
        return "Global Estate Hub Properties"


class PropertyDetailAPIView(RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get_view_name(self):
        return "Property Details"


class TourSchedulesAPIView(ListAPIView):
    queryset = TourSchedule.objects.all()
    serializer_class = TourScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "property": ["exact"],
        "property__title": ["exact"],
        "customer": ["exact"],
        "customer__username": ["exact"],
    }

    def get_view_name(self):
        return "Global Estate Hub Tour Schedules"


class TourScheduleDetailAPIView(RetrieveAPIView):
    queryset = TourSchedule.objects.all()
    serializer_class = TourScheduleSerializer

    def get_view_name(self):
        return "Tour Schedule Details"


class ReviewsAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "property": ["exact"],
        "property__title": ["exact"],
        "user": ["exact"],
        "user__username": ["exact"],
    }

    def get_view_name(self):
        return "Global Estate Hub Reviews"


class ReviewDetailAPIView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_view_name(self):
        return "Review Details"
