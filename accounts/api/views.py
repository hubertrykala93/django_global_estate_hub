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
    filterset_fields = {
        "is_active": ["exact"],
        "is_agent": ["exact"],
        "account_type": ["exact"],
    }

    def get_view_name(self):
        return "Global Estate Hub Registered Users"


class UserDetailsAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_view_name(self):
        return "User Detail"


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
