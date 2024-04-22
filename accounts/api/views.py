from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from accounts.models import User, Individual, Business
from .serializers import (
    UserSerializer,
    IndividualProfileSerializer,
    BusinessProfileSerializer,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


@api_view(http_method_names=["GET"])
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
            "Search User Individual Profile by Gender": "api/v1/users/individuals?gender=gender",
            "Search User Individual Profile by Country": "api/v1/users/individuals?country=country",
            "Search User Individual Profile by Province": "api/v1/users/individuals?province=province",
            "Search User Individual Profile by City": "api/v1/users/individuals?city=city",
            "Search User Business Profile by Country": "api/v1/users/business?country=country",
            "Search User Business Profile by Province": "api/v1/users/business?province=province",
            "Search User Business Profile by City": "api/v1/users/business?city=city",
            "User Individual Profile Details": "api/v1/users/individuals/pk",
            "User Individual Profile Update": "api/v1/users/individuals/pk/update",
            "User Individual Profile Delete": "api/v1/users/individuals/pk/delete",
            "User Business Profile Details": "api/v1/users/business/pk",
            "User Business Profile Update": "api/v1/users/business/pk/update",
            "User Business Profile Delete": "api/v1/users/business/pk/delete",
            # "User Comments": "api/v1/users/pk/comments",
            # "User Comment Details": "api/v1/users/pk/comment/pk",
            # "Comments Liked by User": "api/v1/users/liked-comments",
            # "Comments Disliked by User": "api/v1/users/disliked-comments",
            "All articles": "api/v1/articles",
            "Search Article by Category": "api/v1/articles?category__name=category_name",
            "Search Article by Tag": "api/v1/articles?tag=tag_name&tag=tag_name",
            "Article Details": "api/v1/article/slug",
            # "Article Comments": "api/v1/blog/article/pk/comments",
            "All Comments": "api/v1/comments",
            "Comment Details": "api/v1/comments/pk",
            # "Comment Create": "api/v1/blog/comment/create",
            # "Comment Update": "api/v1/blog/comment/pk/update",
            # "Comment Delete": "api/v1/blog/comment/pk/delete",
            # "All Liked Comments": "api/v1/blog/comments/liked",
            # "All Disliked Comments": "api/v1/blog/comments/disliked",
            # "Search Comment by Is Active": "api/v1/blog/comments?active=is_active",
        },
        status=status.HTTP_200_OK,
    )


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


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_view_name(self):
        return "Creating a New User"

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_view_name(self):
        return "Updating an Existing User."


class UserDeleteAPIView(RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_view_name(self):
        return "Deleting an Existing User."


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


class UserIndividualProfileUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Individual.objects.all()
    serializer_class = IndividualProfileSerializer

    def get_view_name(self):
        return "User Individual Profile Update"


class UserIndividualProfileDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Individual.objects.all()
    serializer_class = IndividualProfileSerializer

    def get_view_name(self):
        return "User Individual Profile Delete"


class UserBusinessProfileDetailsAPIView(RetrieveAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessProfileSerializer

    def get_view_name(self):
        return "User Business Profile Details"


class UserBusinessProfileUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessProfileSerializer

    def get_view_name(self):
        return "User Business Profile Update"


class UserBusinessProfileDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessProfileSerializer

    def get_view_name(self):
        return "User Business Profile Delete"
