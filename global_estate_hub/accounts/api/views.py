from rest_framework.generics import ListAPIView
from accounts.models import User, Individual, Business
from .serializers import UserSerializer, IndividualProfileSerializer, BusinessProfileSerializer


class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_view_name(self):
        return 'Global Estate Hub Users'

    def get_view_description(self, html=False):
        return 'API view with all registered users on the Global Estate Hub platform.'


class IndividualProfileAPIView(ListAPIView):
    queryset = Individual.objects.all()
    serializer_class = IndividualProfileSerializer

    def get_view_name(self):
        return 'Global Estate Hub Individual Profiles'

    def get_view_description(self, html=False):
        return 'API view with all individual profiles on the Global Estate Hub platform.'


class BusinessProfileAPIView(ListAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessProfileSerializer

    def get_view_name(self):
        return 'Global Estate Hub Business Profiles'

    def get_view_description(self, html=False):
        return 'API view with all business profiles on the Global Estate Hub platform.'
