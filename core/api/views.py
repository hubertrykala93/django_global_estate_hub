from .serializers import NewsletterSerializer
from core.models import Newsletter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from datetime import datetime


@api_view(http_method_names=["GET"])
def api_endpoints(request):
    return Response(
        data={
            "Main": {
                "Newsletters": "api/v1/newsletters",
                "Ordering": "",
                "Create(POST)": "",
                "Update(PUT)": "",
                "Delete(DELETE)": "",
            },
            "Accounts": {
                "Users": {
                    "Registered Users": "api/v1/users",
                    "Registered User Details": "api/v1/users/<int:pk>",
                    "Registered Users by Account Type": "api/v1/users?account_type={account_type}",
                    "Registered Users by Is Agent": "api/v1/users?is_agent={is_agent}",
                    "Registered Users by Is Verified": "api/v1/users?is_verified={is_verified}",
                },
                "Profiles": {
                    "Individual Profiles": "api/v1/users/individuals",
                    "Individual Profile Details": "api/v1/users/individuals/<int:pk>",
                    "Individual Profiles by Gender": "api/v1/users/individuals?gender={gender}",
                    "Individual Profiles by Country": "api/v1/users/individuals?country={country}",
                    "Individual Profiles by Province": "api/v1/users/individuals?province={province}",
                    "Individual Profiles by City": "api/v1/users/individuals?city={city}",
                    "Business Profiles": "api/v1/users/business",
                    "Business Profile Details": "api/v1/users/business/<int:pk>",
                    "Business Profiles by Country": "api/v1/users/business?country={country}",
                    "Business Profiles by Province": "api/v1/users/business?province={province}",
                    "Business Profiles by City": "api/v1/users/business?city={city}",
                },
            },
            "Blog": {
                "Articles": {
                    "Articles": "api/v1/articles",
                    "Article Details": "api/v1/articles/<int:pk>",
                    "Articles by Category ID": "api/v1/articles?category__id={category.id}",
                    "Articles by Category Name": "api/v1/articles?category__name={category.name}",
                },
                "Comments": {
                    "Comments": "api/v1/comments",
                    "Comment Details": "api/v1/comments/<int:pk>",
                    "Comments by User ID": "api/v1/comments?user__id={user.id}",
                    "Comments by User Username": "api/v1/comments?user__username={user.username}",
                    "Comments by Is Active": "api/v1/comments?active={active}",
                    "Comments by Level": "api/v1/comments?level={level}",
                    "Article Comments by Article ID": "api/v1/comments?article__id={article.id}",
                    "Article Comments by Article Title": "api/v1/comments?article__title={article.title}",
                },
            },
            "Properties": {
                "Properties": {
                    "Properties": "api/v1/properties",
                    "Property Details": "api/v1/properties/<int:pk>",
                    "Search Property Titles using a Keyword": "api/v1/properties?search={keyword}",
                    "Sorting Properties by Title Ascending": "api/v1/properties?ordering=title",
                    "Sorting Properties by Title Descending": "api/v1/properties?ordering=-title",
                    "Sorting Properties by Price Ascending": "api/v1/properties?ordering=price",
                    "Sorting Properties by Price Descending": "api/v1/properties?ordering=-price",
                    "Sorting Properties by Featured Ascending": "api/v1/properties?ordering=is_featured",
                    "Sorting Properties by Featured Descending": "api/v1/properties?ordering=-is_featured",
                    "Properties by User ID": "api/v1/properties?user__id={user.id}",
                    "Properties by User Username": "api/v1/properties?user__username={user.username}",
                    "Properties by Listing Status ID": "api/v1/properties?listing_status__id={listing_status.id}",
                    "Properties by Listing Status Name": "api/v1/properties?listing_status__name={listing_status.name}",
                    "Properties by Category ID": "api/v1/properties?category__id={category.id}",
                    "Properties by Category Name": "api/v1/properties?category__name={category.name}",
                    "Properties by Year of Built": "api/v1/properties?year_of_built={year_of_built}",
                    "Properties by Year of Built Range Ending at a Specific Year of Built": "api/v1/properties?max_year={year_of_built}",
                    "Properties by Year of Built Range Starting from a Specific Year of Built": "api/v1/properties?min_year={year_of_built}",
                    "Properties within a Specific Year of Built Range": "api/v1/properties?min_year={year_of_built}&max_year={year_of_built}",
                    "Properties by Price": "api/v1/properties?price={price}",
                    "Properties by Price Range Ending at a Specific Price": "api/v1/properties?max_price={price}",
                    "Properties by Price Range Starting from a Specific Price": "api/v1/properties?min_price={price}",
                    "Properties within a Specific Price Range": "api/v1/properties?min_price={price}&max_price={price}",
                    "Properties by Number of Bedrooms": "api/v1/properties?number_of_bedrooms={number_of_bedrooms}",
                    "Properties by Number of Bedrooms Range Ending at a Specific Number of Bedrooms": "api/v1/properties?max_bedrooms={number_of_bedrooms}",
                    "Properties by Number of Bedrooms Range Starting from a Specific Number of Bedrooms": "api/v1/properties?min_bedrooms={number_of_bedrooms}",
                    "Properties within a Specific Number of Bedrooms Range": "api/v1/properties?min_bedrooms={number_of_bedrooms}&max_bedrooms={number_of_bedrooms}",
                    "Properties by Number of Bathrooms": "api/v1/properties?number_of_bathrooms={number_of_bathrooms}",
                    "Properties by Number of Bathrooms Range Ending at a Specific Number of Bathrooms": "api/v1/properties?max_bathrooms={number_of_bathrooms}",
                    "Properties by Number of Bathrooms Range Starting from a Specific Number of Bathrooms": "api/v1/properties?min_bathrooms={number_of_bathrooms}",
                    "Properties within a Specific Number of Bathrooms Range": "api/v1/properties?min_bathrooms={number_of_bathrooms}&max_bathrooms={number_of_bathrooms}",
                    "Properties by Square Meters": "api/v1/properties?square_meters={square_meters}",
                    "Properties by Square Meters Range Ending at a Specific Square Meters": "api/v1/properties?max_square={square_meters}",
                    "Properties by Square Meters Range Starting from a Specific Square Meters": "api/v1/properties?min_square={square_meters}",
                    "Properties within a Specific Square Meters Range": "api/v1/properties?min_square={square_meters}&max_square={square_meters}",
                    "Properties by Parking Space": "api/v1/properties?price={parking_space}",
                    "Properties by Parking Space Range Ending at a Specific Parking Space": "api/v1/properties?max_space={parking_space}",
                    "Properties by Parking Space Range Starting from a Specific Parking Space": "api/v1/properties?min_space={parking_space}",
                    "Properties within a Specific Parking Space Range": "api/v1/properties?min_space={parking_space}&max_space={parking_space}",
                    "Properties by City ID": "api/v1/properties?city__id={city.id}",
                    "Properties by City Name": "api/v1/properties?city__name={city.name}",
                    "Properties by Province": "api/v1/properties?province={province}",
                    "Properties by Country": "api/v1/properties?country={country}",
                    "Properties by Is Featured": "api/v1/properties?is_featured={is_featured}",
                },
                "Reviews": {
                    "Reviews": "api/v1/reviews",
                    "Review Details": "api/v1/reviews/<int:pk>",
                    "Reviews by User ID": "api/v1/reviews?user__id={user.id}",
                    "Reviews by User Username": "api/v1/reviews?user__username={user.username}",
                    "Reviews by Property ID": "api/v1/reviews?property__id={property.id}",
                    "Reviews by Property Title": "api/v1/reviews?property__title={property.title}",
                },
                "Tour Schedules": {
                    "Tour Schedules": "api/v1/tour-schedules",
                    "Tour Schedule Details": "api/v1/tour-schedules/<int:pk>",
                    "Tour Schedules by Customer ID": "api/v1/tour-schedules?customer__id={customer.id}",
                    "Tour Schedules by Customer Username": "api/v1/tour-schedules?customer__username={customer.username}",
                    "Tour Schedules by Property ID": "api/v1/tour-schedules?property__id={property.id}",
                    "Tour Schedules by Property Title": "api/v1/tour-schedules?property__title={property.title}",
                },
            },
        },
        status=status.HTTP_200_OK
    )


class NewsletterAPIView(ListAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["subscribed_at", "email"]

    def get_view_name(self):
        return "Global Estate Hub Newsletters"


class NewsletterCreateAPIView(CreateAPIView):
    serializer_class = NewsletterSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        serializer = self.get_serializer(data=data)

        if Newsletter.objects.filter(email=data.get("email")).exists():
            return Response(
                data={
                    "message": "The newsletter already exists.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            self.perform_create(serializer=serializer)
            headers = self.get_success_headers(data=serializer.data)

            return Response(
                data={
                    "message": "The newsletter has been added successfully.",
                    "newsletter": serializer.data,
                    "headers": headers,
                },
                status=status.HTTP_201_CREATED,
                headers=headers,
            )

        else:
            return Response(
                data={
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_success_headers(self, data):
        try:
            return {
                "Location": str(data["id"])
            }
        except (TypeError, KeyError):
            return {}


class NewsletterUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        partial = kwargs.get("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(instance=instance, partial=partial, data=data)

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
                data={
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_success_headers(self, data):
        try:
            return {
                "Location": str(data["id"])
            }
        except (TypeError, KeyError):
            return {}


class NewsletterDeleteAPIView(RetrieveDestroyAPIView):
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()

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
                    "errors": f"There was an error while deleting the newsletter.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
