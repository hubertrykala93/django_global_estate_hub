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
    UserCreateSerializer,
    UserUpdateSerializer,
    IndividualProfileSerializer,
    BusinessProfileSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from datetime import datetime
from .permissions import IsAdminOrOwner


class UsersAPIView(ListAPIView):
    """
    API view allowing to retrieve all registered users.
    """

    queryset = User.objects.all()
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
    """
    API view allowing to retrieve a specific user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_view_name(self):
        return "User Details"


class UserCreateAPIView(CreateAPIView):
    """
    API view allowing to create a new user.
    """

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrOwner]

    def get_view_name(self):
        return "User Create"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            headers = get_success_headers(data=serializer.data)

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


class UserUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view allowing partial or full update of a specific User object.
    """

    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrOwner]

    def get_view_name(self):
        return "User Update"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserUpdateSerializer(
            instance=instance, data=request.data
        )

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            headers = get_success_headers(data=serializer.data)

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


class UserDeleteAPIView(RetrieveDestroyAPIView):
    """
    API view allowing deletion of a specific user.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrOwner]

    def get_view_name(self):
        return "User Delete"

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
    """
    API view allowing to retrieve all individual profiles.
    """

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
    """
    API view allowing to retrieve all business profiles.
    """

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
    """
    API view allowing to retrieve a specific individual profile.
    """

    queryset = Individual.objects.all()
    serializer_class = IndividualProfileSerializer

    def get_view_name(self):
        return "Individual Profile Details"


class UserIndividualProfileUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view allowing partial or full update of a specific Individual Profile object.
    """

    serializer_class = IndividualProfileSerializer
    queryset = Individual.objects.all()
    permission_classes = [IsAdminOrOwner]

    def get_view_name(self):
        return "Individual Profile Update"

    def update(self, request, *args, **kwargs):
        partial = kwargs.get("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            data=request.data, instance=instance, partial=partial
        )

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            headers = get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "Profile has been successfully updated.",
                    "profile": serializer.data,
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


class UserIndividualProfileDeleteAPIView(RetrieveDestroyAPIView):
    """
    API view allowing deletion of a specific individual profile.
    """

    serializer_class = IndividualProfileSerializer
    lookup_field = "pk"
    queryset = Individual.objects.all()
    permission_classes = [IsAdminOrOwner]

    def get_view_name(self):
        return "Individual Profile Delete"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        temp_id = instance.id

        try:
            self.perform_destroy(instance=instance)

            return Response(
                data={
                    "message": "Profile has been successfully deleted.",
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


class UserBusinessProfileDetailsAPIView(RetrieveAPIView):
    """
    API view allowing to retrieve a specific business profile.
    """

    queryset = Business.objects.all()
    serializer_class = BusinessProfileSerializer

    def get_view_name(self):
        return "Business Profile Details"


class UserBusinessProfileUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view allowing partial or full update of a specific Business Profile object.
    """

    serializer_class = BusinessProfileSerializer
    queryset = Business.objects.all()
    permission_classes = [IsAdminOrOwner]

    def get_view_name(self):
        return "Business Profile Update"

    def update(self, request, *args, **kwargs):
        partial = kwargs.get("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            data=request.data, instance=instance, partial=partial
        )

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            headers = get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "Profile has been successfully updated.",
                    "profile": serializer.data,
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


class UserBusinessProfileDeleteAPIView(RetrieveDestroyAPIView):
    """
    API view allowing deletion of a specific business profile.
    """

    serializer_class = BusinessProfileSerializer
    queryset = Business.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAdminOrOwner]

    def get_view_name(self):
        return "Business Profile Delete"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        temp_id = instance.id

        try:
            self.perform_destroy(instance=instance)

            return Response(
                data={
                    "message": "Profile has been successfully deleted.",
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


def get_success_headers(data):
    try:
        return {"location": str(data["id"])}
    except (TypeError, KeyError):
        return {}
