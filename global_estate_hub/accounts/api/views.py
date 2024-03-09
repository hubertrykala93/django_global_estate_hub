from rest_framework.generics import ListAPIView
from accounts.models import User, Individual, Business
from .serializers import UserSerializer, IndividualProfileSerializer, BusinessProfileSerializer


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IndividualProfileList(ListAPIView):
    queryset = Individual.objects.all()
    serializer_class = IndividualProfileSerializer


class BusinessProfileList(ListAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessProfileSerializer
