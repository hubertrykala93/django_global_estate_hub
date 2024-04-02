from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView
from accounts.models import User, Individual, Business
from .serializers import UserSerializer, IndividualProfileSerializer, BusinessProfileSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(http_method_names=['GET'])
def api_endpoints(request):
    return Response(
        data={
            "Users": "api/v1/users",
            "Search User by Is Agent": "api/v1/users/?is-agent=is_agent",
            "Search User by Date Joined": "api/v1/users/?date-joined=date_joined",
            "User Details": "api/v1/users/pk",
            "User Create": "api/v1/users/create",
            "User Update": "api/v1/users/pk/update",
            "User Delete": "api/v1/users/pk/delete",
            "User Profiles": "api/v1/users/profiles",
            "Search User Profile by Gender": "api/v1/users/profiles/?gender=gender",
            "Search User Profile by Country": "api/v1/users/profiles/?country=country",
            "Search User Profile by Province": "api/v1/users/profiles/?province=province",
            "Search User Profile by City": "api/v1/users/profiles/?city=city",
            "User Profile Details": "api/v1/users/?account-type=account_type/pk",
            "User Profile Create": "api/v1/users/profiles/create",
            "User Profile Update": "api/v1/users/?account-type=account_type/pk/update",
            "User Profile Delete": "api/v1/users/?account-type=account_type/pk/delete",
        },
        status=status.HTTP_200_OK)


class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_view_name(self):
        return 'Global Estate Hub Users'

    def get_view_description(self, html=False):
        return 'API view with all registered users on the Global Estate Hub platform.'


class UserDetailsAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'pk'
    serializer_class = UserSerializer

    def get_view_name(self):
        return 'Global Estate Hub User Details'

    def get_view_description(self, html=False):
        return 'API view with details of the selected user on the Global Estate Hub platform.'


class UserCreateAPIView(CreateAPIView):
    # queryset = User.objects.all()
    # serializer_class = UserCreateSerializer
    #
    # def get_view_name(self):
    #     return 'Global Estate Hub User Create'
    #
    # def get_view_description(self, html=False):
    #     return 'API view with the ability to create a new user on the Global Estate Hub platform.'
    pass


class UserUpdateAPIView(RetrieveUpdateAPIView):
    # queryset = User.objects.all()
    # serializer_class = UserUpdateSerializer
    # lookup_field = 'pk'
    #
    # def get_view_name(self):
    #     return 'Global Estate Hub User Update'
    #
    # def get_view_description(self, html=False):
    #     return 'API view with the ability to update an existing user on the Global Estate Hub platform.'
    pass


class UserDeleteAPIView(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def get_view_name(self):
        return 'Global Estate Hub User Delete'

    def get_view_description(self, html=False):
        return 'API view with the ability do delete an existing user on the Global Estate Hub platform.'


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
