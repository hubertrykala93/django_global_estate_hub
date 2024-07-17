from .serializers import NewsletterSerializer, NewsletterCreateSerializer
from core.models import Newsletter
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from .permissions import IsAdminOnly


@api_view(http_method_names=["GET"])
def api_endpoints(request):
    response = {
        "General": {
            "Method": "GET",
            "URL": "api/v1",
            "Description": "Endpoints",
        },
        "Newsletters": [
            {
                "Method": "GET",
                "URL": "api/v1/newsletters",
                "Description": "Retrieve all newsletters.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/newsletters/<int:pk>",
                "Description": "Retrieve newsletter with a specific ID.",
            },
            {
                "Method": "POST",
                "URL": "api/v1/newsletters/create-newsletter",
                "Description": "Create a new newsletter.",
            },
            {
                "Method": "PATCH/PUT",
                "URL": "api/v1/newsletters/update-newsletter/<int:pk>",
                "Description": "Update newsletter with specific ID.",
            },
            {
                "Method": "DELETE",
                "URL": "api/v1/newsletters/delete-newsletter/<int:pk>",
                "Description": "Deleting newsletter with specific ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/newsletters?ordering={subscribed_at}",
                "Description": "Sorts newsletters by subscribed at using the chosen method (ascending, descending) and retrieves them.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/newsletters?ordering={email}",
                "Description": "Sorts newsletters by email using the chosen method (ascending, descending) and retrieves them.",
            },
        ],
        "users": [
            {
                "Method": "GET",
                "URL": "api/v1/users/",
                "Description": "Retrieve all users.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users/<int:pk>",
                "Description": "Retrieve user with a specific ID.",
            },
            {
                "Method": "POST",
                "URL": "api/v1/users/create-user",
                "Description": "Create a new user.",
            },
            {
                "Method": "PATCH/PUT",
                "URL": "api/v1/users/update-user/<int:pk>",
                "Description": "Update user with specific ID.",
            },
            {
                "Method": "DELETE",
                "URL": "api/v1/users/delete-user/<int:pk>",
                "Description": "Deleting user with specific ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users?ordering=date_joined",
                "Description": "Sorts users by date joined using the chosen method (ascending, descending) and retrieves them.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users?ordering=username",
                "Description": "Sorts users by username using the chosen method (ascending, descending) and retrieves them.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users?ordering=email",
                "Description": "Sorts users by email using the chosen method (ascending, descending) and retrieves them.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users?ordering=last_login",
                "Description": "Sorts users by last login using the chosen method (ascending, descending) and retrieves them.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users?account_type={account_type}",
                "Description": "Retrieve all users with a specific account type.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users?is_agent={is_agent}",
                "Description": "Retrieve all users who are agents.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users?is_verified={is_verified}",
                "Description": "Retrieve all verified users.",
            },
        ],
        "Invididual Profiles": [
            {
                "Method": "GET",
                "URL": "api/v1/individuals",
                "Description": "Retrieve all individual profiles.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users/individuals/<int:pk>",
                "Description": "Retrieve user's individual profile with a specific ID.",
            },
            {
                "Method": "PATCH/PUT",
                "URL": "api/v1/individuals/update-profile/<int:pk>",
                "Description": "Update individual profile with a specific ID.",
            },
            {
                "Method": "DELETE",
                "URL": "api/v1/users/individuals/delete-profile/<int:pk>",
                "Description": "Deleting individual profile with a specific ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users/individuals?gender={gender}",
                "Description": "Retrieve all individual user profiles with a specific gender.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users/individuals?country={country}",
                "Description": "Retrieve all individual user profiles with a specific country.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users/individuals?province={province}",
                "Description": "Retrieve all individual user profiles with a specific province.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users/individuals?city={city}",
                "Description": "Retrieve all individual user profiles with a specific city.",
            },
        ],
        "Business Profiles": [
            {
                "Method": "GET",
                "URL": "api/v1/users/business",
                "Description": "Retrieve all business profiles.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users/business/<int:pk>",
                "Description": "Retrieve user's business profile with a specific ID.",
            },
            {
                "Method": "PATCH/PUT",
                "URL": "api/v1/users/business/update-profile/<int:pk>",
                "Description": "Update business profile with a specific ID.",
            },
            {
                "Method": "DELETE",
                "URL": "api/v1/users/business/delete-profile/<int:pk>",
                "Description": "Deleting business profile with a specific ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users/business?country={country}",
                "Description": "Retrieve all business user profiles with a specific country.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users/business?province={province}",
                "Description": "Retrieve all business user profiles with a specific province.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/users/business?city={city}",
                "Description": "Retrieve all business user profiles with a specific city.",
            },
        ],
        "Articles": [
            {
                "Method": "GET",
                "URL": "api/v1/articles",
                "Description": "Retrieve all articles.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/articles/<int:pk>",
                "Description": "Retrieve article with a specific ID.",
            },
            {
                "Method": "POST",
                "URL": "api/v1/articles/create-article",
                "Description": "Create a new article.",
            },
            {
                "Method": "PATCH/PUT",
                "URL": "api/v1/articles/update-article/<int:pk>",
                "Description": "Update article with specific ID.",
            },
            {
                "Method": "DELETE",
                "URL": "api/v1/articles/delete-article/<int:pk>",
                "Description": "Deleting article with specific ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/articles?search={keyword}",
                "Description": "Search and retrieve articles by title and content using a keyword.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/articles?ordering=date_posted",
                "Description": "Sorts articles by date_posted at using the chosen method (ascending, descending) and retrieves them.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/articles?ordering=title",
                "Description": "Sorts articles by title at using the chosen method (ascending, descending) and retrieves them.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/articles?category__id={category.id}",
                "Description": "Retrieve all articles with a specific category ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/articles?category__name={category.name}",
                "Description": "Retrieve all articles with a specific category name.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/article-categories",
                "Description": "Retrieve all article categories.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/article-tags",
                "Description": "Retrieve all article tags.",
            },
        ],
        "comments": [
            {
                "Method": "GET",
                "URL": "api/v1/comments",
                "Description": "Retrieve all comments.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/comments/<int:pk>",
                "Description": "Retrieve comment with a specific ID.",
            },
            {
                "Method": "POST",
                "URL": "api/v1/comments/create-comment",
                "Description": "Create a new comment.",
            },
            {
                "Method": "PATCH/PUT",
                "URL": "api/v1/comments/update-comment/<int:pk>",
                "Description": "Update comment with specific ID.",
            },
            {
                "Method": "DELETE",
                "URL": "api/v1/comments/delete-comment/<int:pk>",
                "Description": "Deleting comment with specific ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/comments?user__id={user.id}",
                "Description": "Retrieve comments posted by a specific user ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/comments?user__username={user.username}",
                "Description": "Retrieve comments posted by a specific user username.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/comments?active={active}",
                "Description": "Retrieve all active comments.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/comments?level={level}",
                "Description": "Retrieve comments by a specific level.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/comments?article__id={article.id}",
                "Description": "Retrieve comments under an article with a specific ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/comments?article__title={article.title}",
                "Description": "Retrieve comments under an article with a specific title.",
            },
        ],
        "Listing Statuses": [
            {
                "Method": "GET",
                "URL": "api/v1/listing-statuses",
                "Description": "Retrieve all listing statuses.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/listing-statuses/<int:pk>",
                "Description": "Retrieve listing status with a specific ID.",
            },
            {
                "Method": "POST",
                "URL": "api/v1/listing-statuses/create-listing-status",
                "Description": "Create a new listing status.",
            },
            {
                "Method": "PATCH/PUT",
                "URL": "api/v1/listing-statuses/update-listing-status/<int:pk>",
                "Description": "Update listing status with specific ID.",
            },
            {
                "Method": "DELETE",
                "URL": "api/v1/listing-statuses/delete-listing-status/<int:pk>",
                "Description": "Deleting listing status with specific ID.",
            },
        ],
        "Categories": [
            {
                "Method": "GET",
                "URL": "api/v1/categories",
                "Description": "Retrieve all categories.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/categories/<int:pk>",
                "Description": "Retrieve category with a specific ID.",
            },
            {
                "Method": "POST",
                "URL": "api/v1/categories/create-category",
                "Description": "Create a new category.",
            },
            {
                "Method": "PATCH/PUT",
                "URL": "api/v1/categories/update-category/<int:pk>",
                "Description": "Update category with specific ID.",
            },
            {
                "Method": "DELETE",
                "URL": "api/v1/categories/delete-category/<int:pk>",
                "Description": "Deleting category with specific ID.",
            },
        ],
        "Properties": [
            {
                "Method": "GET",
                "URL": "api/v1/properties",
                "Description": "Retrieve all properties.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/<int:pk>",
                "Description": "Retrieve property with a specific ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties?search={keyword}",
                "Description": "Search and retrieve properties by title using a keyword.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/ordering=title",
                "Description": "Sorts properties by title using the chosen method (ascending, descending) and retrieves them.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/ordering=price",
                "Description": "Sorts properties by price using the chosen method (ascending, descending) and retrieves them.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/ordering=featured",
                "Description": "Sorts properties by featured using the chosen method (ascending, descending) and retrieves them.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/user__id={user.id}",
                "Description": "Retrieve properties posted by a specific user ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/user__username={user.username}",
                "Description": "Retrieve properties posted by a specific user username.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/listing_status__id={listing_status.id}",
                "Description": "Retrieve properties with a specific listing status ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/listing_status__name={listing_status.id}",
                "Description": "Retrieve properties with a specific listing status name.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/category__id={category.id}",
                "Description": "Retrieve properties with a specific category ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/category__id={category.id}&category__id={category.id}",
                "Description": "Retrieve properties with a specific category IDs.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/category__name={category.name}",
                "Description": "Retrieve properties with a specific category name.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/category__name={category.name}&category__name={category.name}",
                "Description": "Retrieve properties with a specific category names.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/year_of_built={year_of_built}",
                "Description": "Retrieve properties with a specific year of built.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/max_year={year_of_built}",
                "Description": "Retrieve all properties up to a specified maximum year of built.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/min_year={year_of_built}",
                "Description": "Retrieve all properties from a specified minimum year of built.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/min_year={year_of_built}&max_year={year_of_built}",
                "Description": "Retrieve all properties within the specified ranges of construction year.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/price={price}",
                "Description": "Retrieve properties with a specific price.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/max_price={price}",
                "Description": "Retrieve all properties up to a specified maximum price.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/min_price={price}",
                "Description": "Retrieve all properties from a specified minimum price.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/min_price={price}&max_price={price}",
                "Description": "Retrieve all properties within the specified ranges of price.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/number_of_bedrooms={number_of_bedrooms}",
                "Description": "Retrieve properties with a specific number of bedrooms.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/max_bedrooms={number_of_bedrooms}",
                "Description": "Retrieve all properties up to a specified maximum number of bedrooms.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/min_bedrooms={number_of_bedrooms}",
                "Description": "Retrieve all properties from a specified minimum number of bedrooms.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/min_bedrooms={number_of_bedrooms}&max_bedrooms={number_of_bedrooms}",
                "Description": "Retrieve all properties within the specified ranges of number of bedrooms.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/number_of_bathrooms={number_of_bathrooms}",
                "Description": "Retrieve properties with a specific number of bathrooms.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/max_bathrooms={number_of_bathrooms}",
                "Description": "Retrieve all properties up to a specified maximum number of bathrooms.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/min_bathrooms={number_of_bathrooms}",
                "Description": "Retrieve all properties from a specified minimum number of bathrooms.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/min_bathrooms={number_of_bathrooms}&max_bathrooms={number_of_bathrooms}",
                "Description": "Retrieve all properties within the specified ranges of number of bathrooms.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/square_meters={square_meters}",
                "Description": "Retrieve properties with a specific square meters.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/max_square={square_meters}",
                "Description": "Retrieve all properties up to a specified maximum square meters.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/min_square={square_meters}",
                "Description": "Retrieve all properties from a specified minimum square meters.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/min_square={square_meters}&max_square={square_meters}",
                "Description": "Retrieve all properties within the specified ranges of square meters.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/parking_space={parking_space}",
                "Description": "Retrieve properties with a specific parking space.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/max_space={parking_space}",
                "Description": "Retrieve all properties up to a specified maximum parking space.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/min_space={parking_space}",
                "Description": "Retrieve all properties from a specified minimum parking space.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/min_space={parking_space}&max_space={parking_space}",
                "Description": "Retrieve all properties within the specified ranges of parking space.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/city__id={city.id}",
                "Description": "Retrieve properties with a specific city ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/city__name={city.name}",
                "Description": "Retrieve properties with a specific city name.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/province={province}",
                "Description": "Retrieve properties with a specific province.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/country={country}",
                "Description": "Retrieve properties with a specific country.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/properties/is_featured={is_featured}",
                "Description": "Retrieve featured or non-featured properties.",
            },
        ],
        "Reviews": [
            {
                "Method": "GET",
                "URL": "api/v1/reviews",
                "Description": "Retrieve all reviews.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/reviews/<int:pk>",
                "Description": "Retrieve review with a specific ID.",
            },
            {
                "Method": "POST",
                "URL": "api/v1/reviews/create-review",
                "Description": "Create a new review.",
            },
            {
                "Method": "PATCH/PUT",
                "URL": "api/v1/reviews/update-review/<int:pk>",
                "Description": "Update review with specific ID.",
            },
            {
                "Method": "DELETE",
                "URL": "api/v1/reviews/delete-reviews/<int:pk>",
                "Description": "Deleting review with specific ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/reviews/user__id={user.id}",
                "Description": "Retrieve reviews posted by a specific user ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/reviews/user__username={user.username}",
                "Description": "Retrieve reviews posted by a specific user username.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/reviews/property__id={property.id}",
                "Description": "Retrieve reviews for a property with a specific ID.",
            },
            {
                "Method": "GET",
                "URL": "api/v1/reviews/property__title={property.title}",
                "Description": "Retrieve reviews for a property with a specific property title.",
            },
        ],
    }

    return Response(
        data=response,
        status=status.HTTP_200_OK,
    )


class NewsletterAPIView(ListAPIView):
    """
    API view allowing to retrieve all newsletters.
    """

    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["subscribed_at", "email"]

    def get_view_name(self):
        return "Global Estate Hub Newsletters"


class NewsletterDetailsAPIView(RetrieveAPIView):
    """
    API view allowing to retrieve a specific newsletter.
    """

    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def get_view_name(self):
        return "Newsletter Details"


class NewsletterCreateAPIView(CreateAPIView):
    """
    API view allowing to create a new newsletter.
    """

    serializer_class = NewsletterCreateSerializer
    queryset = Newsletter.objects.all()
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Newsletter Create"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The e-mail address has been added successfully.",
                    "newsletter": serializer.data,
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
            return {
                "location": str(data["id"]),
            }
        except (TypeError, KeyError):
            return {}


class NewsletterUpdateAPIView(RetrieveUpdateAPIView):
    """
    API view allowing partial or full update of a specific Newsletter object.
    """

    serializer_class = NewsletterCreateSerializer
    queryset = Newsletter.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Newsletter Update"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance=instance, data=request.data)

        if serializer.is_valid():
            self.perform_update(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The newsletter has been successfully updated.",
                    "newsletter": serializer.data,
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

    def get_success_headers(self, data):
        try:
            return {
                "location": str(data["id"]),
            }
        except (TypeError, KeyError):
            return {}


class NewsletterDeleteAPIView(RetrieveDestroyAPIView):
    """
    API view allowing deletion of a specific newsletter.
    """

    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    permission_classes = [IsAdminOnly]

    def get_view_name(self):
        return "Newsletter Delete"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        temp_id = instance.id

        try:
            self.perform_destroy(instance=instance)

            return Response(
                data={
                    "message": "The newsletter has been successfully deleted.",
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
