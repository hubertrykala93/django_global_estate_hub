from rest_framework.generics import ListAPIView
from accounts.models import User, Individual, Business
from .serializers import UserSerializer, IndividualProfileSerializer, BusinessProfileSerializer


class UserList(ListAPIView):
    """
    The API view with all registered users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IndividualProfileList(ListAPIView):
    """
    The API view with all individual profiles.
    """
    queryset = Individual.objects.all()
    serializer_class = IndividualProfileSerializer


class BusinessProfileList(ListAPIView):
    """
    The API view with all business profiles.
    """
    queryset = Business.objects.all()
    serializer_class = BusinessProfileSerializer
