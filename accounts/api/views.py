from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from accounts.models import User, Individual, Business
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserSerializer,
    IndividualProfileSerializer,
    BusinessProfileSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from datetime import datetime


class UsersAPIView(ListAPIView):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "is_agent": ["exact"],
        "is_verified": ["exact"],
        "account_type": ["exact"],
    }
    ordering_fields = ["date_joined", "username", "email", "last_login"]

    def get_view_name(self):
        return "Global Estate Hub Registered Users"


class UserDetailsAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_view_name(self):
        return "User Detail"


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        errors = []

        if len(request.data.get("username")) < 1:
            errors.append(
                {
                    "field": "username",
                    "error": "The username field cannot be empty.",
                }
            )

        if len(request.data.get("email")) < 1:
            errors.append(
                {
                    "field": "email",
                    "error": "The e-mail field cannot be empty.",
                }
            )

        if len(request.data.get("password")) < 1:
            errors.append(
                {
                    "field": "password",
                    "error": "The password field cannot be empty."
                }
            )

        if errors:
            return Response(
                data=errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The user has been created successfully.",
                    "user": serializer.data,
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
            return {"location": str(data["id"])}
        except (TypeError, KeyError):
            return {}


class UserUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        partial = kwargs.get("partial", False)
        instance = self.get_object()
        serializer = UserSerializer(
            instance=instance, partial=partial, data=request.data
        )

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The user has been successfully updated.",
                    "user": serializer.data,
                    "headers": headers,
                },
                status=status.HTTP_200_OK,
                headers=headers,
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_success_headers(self, data):
        try:
            return {"Location": str(data["id"])}
        except (TypeError, KeyError):
            return {}


class UserDeleteAPIView(RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        temp_id = instance.id

        try:
            self.perform_destroy(instance=instance)

            return Response(
                data={
                    "message": "The user has been successfully deleted.",
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


class IndividualProfileAPIView(ListAPIView):
    queryset = Individual.objects.all()
    serializer_class = IndividualProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "gender": ["exact"],
        "country": ["exact"],
        "province": ["exact"],
        "city": ["exact"],
    }

    def get_view_name(self):
        return "Global Estate Hub Individual Profiles"


class BusinessProfileAPIView(ListAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "country": ["exact"],
        "province": ["exact"],
        "city": ["exact"],
    }

    def get_view_name(self):
        return "Global Estate Hub Business Profiles"


class UserIndividualProfileDetailsAPIView(RetrieveAPIView):
    queryset = Individual.objects.all()
    serializer_class = IndividualProfileSerializer

    def get_view_name(self):
        return "User Individual Profile Details"


class UserBusinessProfileDetailsAPIView(RetrieveAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessProfileSerializer

    def get_view_name(self):
        return "User Business Profile Details"
