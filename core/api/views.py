from .serializers import NewsletterSerializer, NewsletterCreateSerializer
from core.models import Newsletter
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from .permissions import IsAdminOnly

@api_view(http_method_names=["GET"])
def api_endpoints(request):
    return Response(
        status=status.HTTP_200_OK,
    )


class NewsletterAPIView(ListAPIView):
    """
    API view allowing to retrieve all newsletters.
    """

    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["subscribed_at", "email"]

    def get_view_name(self):
        return "Global Estate Hub Newsletters"


class NewsletterDetailsAPIView(RetrieveAPIView):
    """
    API view allowing to retrieve a specific newsletter.
    """

    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def get_view_name(self):
        return "Newsletter Details"


class NewsletterCreateAPIView(CreateAPIView):
    """
    API view allowing to create a new newsletter.
    """

    serializer_class = NewsletterCreateSerializer
    queryset = Newsletter.objects.all()
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Newsletter Create"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The e-mail address has been added successfully.",
                    "newsletter": serializer.data,
                    "headers": headers,
                },
                status=status.HTTP_201_CREATED,
                headers=headers,
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_success_headers(self, data):
        try:
            return {
                "location": str(data["id"]),
            }
        except (TypeError, KeyError):
            return {}


class NewsletterUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view allowing partial or full update of a specific Newsletter object.
    """

    serializer_class = NewsletterCreateSerializer
    queryset = Newsletter.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Newsletter Update"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(
            instance=instance, data=request.data
        )

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The newsletter has been successfully updated.",
                    "newsletter": serializer.data,
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
                "location": str(data["id"]),
            }
        except (TypeError, KeyError):
            return {}


class NewsletterDeleteAPIView(RetrieveDestroyAPIView):
    """
    API view allowing deletion of a specific newsletter.
    """

    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Newsletter Delete"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        temp_id = instance.id

        try:
            self.perform_destroy(instance=instance)

            return Response(
                data={
                    "message": "The newsletter has been successfully deleted.",
                    "id": temp_id,
                    "deleted_by": self.request.user.username,
                    "deleted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        except Exception:
            return Response(
                data={
                    "error": "There was an error while deleting the newsletter.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
