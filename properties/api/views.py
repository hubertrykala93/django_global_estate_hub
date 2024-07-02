from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView
from properties.models import Property, TourSchedule, Review
from .serializers import PropertySerializer, TourScheduleSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


class PropertyAPIView(ListAPIView):
    """
    API view allowing to retrieve all properties.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ["title"]
    ordering_fields = ["title", "price", "is_featured"]

    def get_view_name(self) -> str:
        return "Global Estate Hub Properties"


class PropertyDetailAPIView(RetrieveAPIView):
    """
    API view allowing to retrieve a specific property.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get_view_name(self):
        return "Property Details"


class TourSchedulesAPIView(ListAPIView):
    """
    API view allowing to retrieve all tour schedules.
    """
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
    """
    API view allowing to retrieve a specific tour schedule.
    """
    queryset = TourSchedule.objects.all()
    serializer_class = TourScheduleSerializer

    def get_view_name(self):
        return "Tour Schedule Details"


class ReviewsAPIView(ListAPIView):
    """
    API view allowing to retrieve all reviews.
    """
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
    """
    API view allowing to retrieve a specific review.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_view_name(self):
        return "Review Details"


class ReviewCreateAPIView(CreateAPIView):
    """
    API view allowing to create a new review.
    """
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_view_name(self):
        return "Review Create"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        errors = []

        if len(request.data.get("rate")) < 1:
            errors.append(
                {
                    "field": "rate",
                    "error": "The rate field cannot be empty.",
                }
            )

        if len(request.data.get("content")) < 1:
            errors.append(
                {
                    "field": "content",
                    "error": "The content field cannot be empty.",
                }
            )

        if errors:
            return Response(
                data=errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            headers = get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The review has been created successfully.",
                    "review": serializer.data,
                    "headers": headers,
                },
                headers=headers,
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReviewUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view allowing partial or full update of a specific Review object.
    """
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_view_name(self):
        return "Review Update"

    def update(self, request, *args, **kwargs):
        partial = self.kwargs.get("partial")
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            headers = get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The review has been updated successfully.",
                    "review": serializer.data,
                    "headers": headers
                },
                headers=headers,
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReviewDeleteAPIView(RetrieveDestroyAPIView):
    """
    API view allowing deletion of a specific review.
    """
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_view_name(self):
        return "Review Delete"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        temp_id = instance.id

        try:
            self.perform_destroy(instance=instance)

            return Response(
                data={
                    "message": "The review has been deleted successfully.",
                    "id": temp_id,
                    "deleted_by": self.request.user.username,
                    "deleted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception:
            return Response(
                data={"error": "There was an error while deleting the user."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TourScheduleCreateAPIView(CreateAPIView):
    """
    API view allowing to create a new tour schedule.
    """
    serializer_class = TourScheduleSerializer
    queryset = TourSchedule.objects.all()

    def get_view_name(self):
        return "Create Tour Schedule"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        errors = []

        if len(request.data.get("date")) < 1:
            errors.append(
                {
                    "field": "date",
                    "error": "The date field cannot be empty.",
                }
            )

        if len(request.data.get("time")) < 1:
            errors.append(
                {
                    "field": "time",
                    "error": "The time field cannot be empty.",
                }
            )

        if len(request.data.get("name")) < 1:
            errors.append(
                {
                    "field": "full_name",
                    "error": "The name field cannot be empty.",
                }
            )

        if len(request.data.get("phone_number")) < 1:
            errors.append(
                {
                    "field": "phone_number",
                    "error": "The phone number field cannot be empty.",
                }
            )

        if len(request.data.get("message")) < 1:
            errors.append(
                {
                    "field": "message",
                    "error": "The message field cannot be empty.",
                }
            )

        if errors:
            return Response(
                data=errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            headers = get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The tour schedule has been created successfully.",
                    "tour_schedule": serializer.data,
                    "headers": headers,
                },
                headers=headers,
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class TourScheduleUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view allowing partial or full update of a specific TourSchedule object.
    """
    serializer_class = TourScheduleSerializer
    queryset = TourSchedule.objects.all()

    def get_view_name(self):
        return "Update Tour Schedule"

    def update(self, request, *args, **kwargs):
        partial = self.kwargs.get("partial")
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            headers = get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The tour schedule has been updated successfully.",
                    "tour_schedule": serializer.data,
                    "headers": headers,
                },
                headers=headers,
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class TourScheduleDeleteAPIView(RetrieveDestroyAPIView):
    """
    API view allowing deletion of a specific tour schedule.
    """
    serializer_class = TourScheduleSerializer
    queryset = TourSchedule.objects.all()

    def get_view_name(self):
        return "Delete Tour Schedule"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        temp_id = instance.id

        try:
            self.perform_destroy(instance=instance)

            return Response(
                data={
                    "message": "The tour schedule has been deleted successfully.",
                    "id": temp_id,
                    "deleted_by": self.request.user.username,
                    "deleted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception:
            return Response(
                data={"error": "There was an error while deleting the user."},
                status=status.HTTP_400_BAD_REQUEST,
            )


def get_success_headers(data):
    try:
        return {"location": str(data["id"])}
    except (TypeError, KeyError):
        return {}
