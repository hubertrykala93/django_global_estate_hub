from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView
from accounts.models import User, Individual, Business
from .serializers import UserSerializer, IndividualProfileSerializer, BusinessProfileSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend


@api_view(http_method_names=['GET'])
def api_endpoints(request):
    return Response(
        data={
            "All Users": "api/v1/users",
            "Search User by Is Agent": "api/v1/users?is_agent=is_agent",
            "Search User by Is Verified": "api/v1/users?is_verified=is_verified",
            "Search User by Account Type": "api/v1/users?account_type=account_type",
            "User Details": "api/v1/users/pk",
            "User Create": "api/v1/users/create",
            "User Update": "api/v1/users/pk/update",
            "User Delete": "api/v1/users/pk/delete",
            "All Profiles": "api/v1/users/profiles",
            # "Search User Profile by Gender": "api/v1/users/profiles?gender=gender",
            # "Search User Profile by Country": "api/v1/users/profiles?country=country",
            # "Search User Profile by Province": "api/v1/users/profiles?province=province",
            # "Search User Profile by City": "api/v1/users/profiles?city=city",
            # "User Profile Details": "api/v1/users?account-type=account_type/pk",
            # "User Profile Create": "api/v1/users/profiles/create",
            # "User Profile Update": "api/v1/users?account-type=account_type/pk/update",
            # "User Profile Delete": "api/v1/users?account-type=account_type/pk/delete",
            # "All articles": "api/v1/blog/articles",
            # "Search Article by Category": "api/v1/blog/articles?category=category_name",
            # "Search Article by Tag": "api/v1/blog/articles?tag=tag_name&tag=tag_name",
            # "Article Details": "api/v1/blog/article/pk",
            # "Article Comments": "api/v1/blog/article/pk/comments",
            # "User Comments": "api/v1/users/pk/comments",
            # "User Comment Details": "api/v1/users/pk/comment/pk",
            # "Comments Liked by User": "api/v1/users/liked-comments",
            # "Comments Disliked by User": "api/v1/users/disliked-comments",
            # "All Comments": "api/v1/blog/comments",
            # "All Liked Comments": "api/v1/blog/comments/liked",
            # "All Disliked Comments": "api/v1/blog/comments/disliked",
            # "Search Comment by Is Active": "api/v1/blog/comments?active=is_active",
            # "Comment Details": "api/v1/blog/comment/pk",
            # "Comment Sub-Comments": "api/v1/blog/comment/pk/sub-comments",
            # "Comment Create": "api/v1/blog/comment/create",
            # "Comment Update": "api/v1/blog/comment/pk/update",
            # "Comment Delete": "api/v1/blog/comment/pk/delete",
        },
        status=status.HTTP_200_OK)


class UsersAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_agent', 'is_verified', 'account_type']

    def get_view_name(self):
        return 'Global Estate Hub Users'

    def get_view_description(self, html=False):
        return 'API view with all registered users on the Global Estate Hub platform.'


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteAPIView(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfilesAPIView(ListAPIView):
    serializer_class_individual = IndividualProfileSerializer
    serializer_class_business = BusinessProfileSerializer

    def get_queryset_individual(self):
        return Individual.objects.all()

    def get_queryset_business(self):
        return Business.objects.all()

    def list(self, request, *args, **kwargs):
        individual = self.serializer_class_individual(instance=self.get_queryset_individual(), many=True)
        business = self.serializer_class_business(instance=self.get_queryset_business(), many=True)

        return Response(data={
            "Individuals": individual.data,
            "Business": business.data,
        })


class UserDetailsAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'pk'
    serializer_class = UserSerializer

    def get_view_name(self):
        return 'Global Estate Hub User Details'

    def get_view_description(self, html=False):
        return 'API view with details of the selected user on the Global Estate Hub platform.'


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
