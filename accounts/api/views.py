from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from accounts.models import User, Individual, Business
from .serializers import (
    UserSerializer,
    IndividualProfileSerializer,
    BusinessProfileSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend


class UsersAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_agent", "is_verified", "account_type"]

    def get_view_name(self):
        return "Registered Users"


class UserDetailsAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_view_name(self):
        return "User Detail"


class IndividualProfileAPIView(ListAPIView):
    queryset = Individual.objects.all()
    serializer_class = IndividualProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["gender", "country", "province", "city"]

    def get_view_name(self):
        return "User Individual Profiles"


class BusinessProfileAPIView(ListAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country", "province", "city"]

    def get_view_name(self):
        return "User Business Profiles"


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
