from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from properties.models import Property, ListingStatus, Category, Review
from .serializers import PropertySerializer, ListingStatusSerializer, \
    ListingStatusCreateSerializer, CategorySerializer, CategoryCreateSerializer, ReviewSerializer, \
    ReviewCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.utils.text import slugify
from .permissions import IsAdminOnly, IsAdminOrOwner


class ListingStatusAPIView(ListAPIView):
    """
    API view allowing to retrieve all listing statuses.
    """
    queryset = ListingStatus.objects.all()
    serializer_class = ListingStatusSerializer

    def get_view_name(self):
        return "Global Estate Hub Listing Statuses"


class ListingStatusDetailAPIView(RetrieveAPIView):
    """
    API view allowing to retrieve a specific listing status.
    """
    queryset = ListingStatus.objects.all()
    serializer_class = ListingStatusSerializer
    lookup_field = "pk"

    def get_view_name(self):
        return "Listing Status Details"


class ListingStatusCreateAPIView(CreateAPIView):
    """
    API view allowing to create a new listing status.
    """
    queryset = ListingStatus.objects.all()
    serializer_class = ListingStatusCreateSerializer
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Listing Status Create"

    def perform_create(self, serializer):
        name = serializer.validated_data.get("name")
        slug = slugify(name)
        serializer.save(slug=slug)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The listing status has been created successfully.",
                    "listing_status": serializer.data,
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

    def get_success_headers(self, data):
        try:
            return {
                "location": str(data["id"])
            }

        except (KeyError, TypeError):
            return {}


class ListingStatusUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view allowing partial or full update of a specific ListingStatus object.
    """
    serializer_class = ListingStatusCreateSerializer
    queryset = ListingStatus.objects.all()
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Listing Status update."

    def perform_update(self, serializer):
        name = serializer.validated_data.get("name")
        slug = slugify(name)
        serializer.save(slug=slug)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, instance=instance)

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The listing status has been updated successfully.",
                    "listing_status": serializer.data,
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

    def get_success_headers(self, data):
        try:
            return {
                "location": str(data["id"])
            }

        except (KeyError, TypeError):
            return {}


class ListingStatusDeleteAPIView(RetrieveDestroyAPIView):
    """
    API view allowing deletion of a specific listing status.
    """
    queryset = ListingStatus.objects.all()
    serializer_class = ListingStatusSerializer
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Listing Status Delete"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        temp_id = instance.id

        try:
            self.perform_destroy(instance=instance)

            return Response(
                data={
                    "message": "The listing status has been deleted successfully.",
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


class CategoryAPIView(ListAPIView):
    """
    API view allowing to retrieve all categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_view_name(self):
        return "Global Estate Hub Categories"


class CategoryDetailAPIView(RetrieveAPIView):
    """
    API view allowing to retrieve a specific category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "pk"

    def get_view_name(self):
        return "Category Details"


class CategoryCreateAPIView(CreateAPIView):
    """
    API view allowing to create a new category.
    """
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Category Create"

    def perform_create(self, serializer):
        name = serializer.validated_data.get("name")
        slug = slugify(name)
        serializer.save(slug=slug)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The category has been created successfully.",
                    "category": serializer.data,
                    "headers": headers,
                },
                headers=headers,
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_success_headers(self, data):
        try:
            return {
                "location": str(data["id"])
            }

        except (TypeError, KeyError):
            return {}


class CategoryUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view allowing partial or full update of a specific Category object.
    """
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Category Update"

    def perform_update(self, serializer):
        name = serializer.validated_data.get("name")
        slug = slugify(name)
        serializer.save(slug=slug)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, instance=instance)

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The category has been updated successfully.",
                    "category": serializer.data,
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

    def get_success_headers(self, data):
        try:
            return {
                "location": str(data["id"])
            }

        except (KeyError, TypeError):
            return {}


class CategoryDeleteAPIView(RetrieveDestroyAPIView):
    """
    API view allowing deletion of a specific category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "pk"
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Category Delete"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        temp_id = instance.id

        try:
            self.perform_destroy(instance=instance)

            return Response(
                data={
                    "message": "The category has been deleted successfully.",
                    "id": temp_id,
                    "deleted_by": self.request.user.username,
                    "deleted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception:
            return Response(
                data={
                    "error": "There was an error while deleting the user."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


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


class ReviewsAPIView(ListAPIView):
    """
    API view allowing to retrieve all reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_view_name(self):
        return "Global Estate Hub Review"


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
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAdminOrOwner]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context.update(
            {
                "request": self.request,
            }
        )

        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

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

    def get_success_headers(self, data):
        try:
            return {
                "location": str(data["id"])
            }

        except (TypeError, KeyError):
            return {}


class ReviewUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view allowing partial or full update of a specific Review object.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminOrOwner]

    def get_view_name(self):
        return "Review Update"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, instance=instance)

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The review has been updated successfully.",
                    "review": serializer.data,
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

    def get_success_headers(self, data):
        try:
            return {
                "location": str(data["id"])
            }

        except (TypeError, KeyError):
            return {}


class ReviewDeleteAPIView(RetrieveDestroyAPIView):
    """
    API view allowing deletion of a specific property.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminOrOwner]

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
                    "deleted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception:
            return Response(
                data={"error": "There was an error while deleting the comment."},
                status=status.HTTP_400_BAD_REQUEST,
            )
