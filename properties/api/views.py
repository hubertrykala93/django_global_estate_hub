from rest_framework.generics import ListAPIView
from properties.models import Property, TourSchedule, Review
from .serializers import PropertySerializer, TourScheduleSerializer, ReviewSerializer


class PropertyAPIView(ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get_view_name(self) -> str:
        return "Global Estate Hub Properties"

    def get_view_description(self, html=False):
        return "API view with all properties on the Global Estate Hub platform."


class TourScheduleAPIView(ListAPIView):
    queryset = TourSchedule.objects.all()
    serializer_class = TourScheduleSerializer

    def get_view_name(self):
        return "Global Estate Hub Tour Schedules"

    def get_view_description(self, html=False):
        return "API view with all tour schedules on the Global Estate Hub platform."


class ReviewAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_view_name(self):
        return "Global Estate Hub Reviews"

    def get_view_description(self, html=False):
        return "API view with all reviews on the Global Estate Hub platform."
