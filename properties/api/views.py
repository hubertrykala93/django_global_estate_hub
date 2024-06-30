from rest_framework.generics import ListAPIView, RetrieveAPIView
from properties.models import Property, TourSchedule, Review
from .serializers import PropertySerializer, TourScheduleSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter
from rest_framework.filters import OrderingFilter, SearchFilter


class PropertyAPIView(ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ["title"]
    ordering_fields = ["title", "price", "is_featured"]

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
        "property__id": ["exact"],
        "property__title": ["exact"],
        "customer__id": ["exact"],
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
        "property__id": ["exact"],
        "property__title": ["exact"],
        "user__id": ["exact"],
        "user__username": ["exact"],
    }

    def get_view_name(self):
        return "Global Estate Hub Reviews"


class ReviewDetailAPIView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_view_name(self):
        return "Review Details"
