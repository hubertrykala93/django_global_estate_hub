from .serializers import NewsletterSerializer
from core.models import Newsletter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(http_method_names=["GET"])
def api_endpoints(request):
    return Response(
        data={
            "All Users": "api/v1/users",
            "All Newsletters": "api/v1/newsletters",
            "Search User by Is Agent": "api/v1/users?is_agent=is_agent",
            "Search User by Is Verified": "api/v1/users?is_verified=is_verified",
            "Search User by Account Type": "api/v1/users?account_type=account_type",
            "User Details": "api/v1/users/pk",
            "Search User Individual Profile by Gender": "api/v1/users/individuals?gender=gender",
            "Search User Individual Profile by Country": "api/v1/users/individuals?country=country",
            "Search User Individual Profile by Province": "api/v1/users/individuals?province=province",
            "Search User Individual Profile by City": "api/v1/users/individuals?city=city",
            "Search User Business Profile by Country": "api/v1/users/business?country=country",
            "Search User Business Profile by Province": "api/v1/users/business?province=province",
            "Search User Business Profile by City": "api/v1/users/business?city=city",
            "User Individual Profile Details": "api/v1/users/individuals/pk",
            "User Business Profile Details": "api/v1/users/business/pk",
            "Search User Comments by User ID": "api/v1/comments?user__id=user_id",
            "Search User Comments by User Username": "api/v1/comments?user__username=user_username",
            "All articles": "api/v1/articles",
            "Search Article by Category": "api/v1/articles?category__name=category_name",
            "Search Article by Tag": "api/v1/articles?tag=tag_name&tag=tag_name",
            "Article Details": "api/v1/article/pk",
            "Article Comments": "api/v1/comments/article__id=article_id",
            "All Comments": "api/v1/comments",
            "Comment Details": "api/v1/comments/pk",
            "Search Comment by Is Active": "api/v1/blog/comments?active=is_active",
            "All Properties": "api/v1/properties",
            "Property Details": "api/v1/property/pk",
            "Search User Properties by User ID": "api/v1/properties?user__id=user_id",
            "Search User Properties by User Username": "api/v1/properties?user__username=user_username",
            "Search Property by Year of Built": "api/v1/properties?year_of_built=year_of_built",
            "Search Property by Year of Built Less than Equal": "api/v1/properties?year_of_built__lte=year_of_built",
            "Search Property by Year of Built Greater than Equal": "api/v1/properties?year_of_built__gte=year_of_built",
            "Search Property by Year of Built Less than": "api/v1/properties?year_of_built__gt=year_of_built",
            "Search Property by Year of Built Greater than": "api/v1/properties?year_of_built__lt=year_of_built",
            "Search Property by Price": "api/v1/properties?price=price",
            "Search Property by Price Less than Equal": "api/v1/properties?price__lte=price",
            "Search Property by Price Greater than Equal": "api/v1/properties?price__gte=price",
            "Search Property by Price Less than": "api/v1/properties?price__gt=price",
            "Search Property by Price Greater than": "api/v1/properties?price__lt=price",
            "Search Property by Number of Bedrooms": "api/v1/properties?number_of_bedrooms=number_of_bedrooms",
            "Search Property by Number of Bedrooms Less than Equal": "api/v1/properties?number_of_bedrooms__lte=number_of_bedrooms",
            "Search Property by Number of Bedrooms Greater than Equal": "api/v1/properties?number_of_bedrooms__gte=number_of_bedrooms",
            "Search Property by Number of Bedrooms Less than": "api/v1/properties?number_of_bedrooms__gt=number_of_bedrooms",
            "Search Property by Number of Bedrooms Greater than": "api/v1/properties?number_of_bedrooms__lt=number_of_bedrooms",
            "Search Property by Number of Bathrooms": "api/v1/properties?number_of_bathrooms=number_of_bathrooms",
            "Search Property by Number of Bathrooms Less than Equal": "api/v1/properties?number_of_bathrooms__lte=number_of_bathrooms",
            "Search Property by Number of Bathrooms Greater than Equal": "api/v1/properties?number_of_bathrooms__gte=number_of_bathrooms",
            "Search Property by Number of Bathrooms Less than": "api/v1/properties?number_of_bathrooms__gt=number_of_bathrooms",
            "Search Property by Number of Bathrooms Greater than": "api/v1/properties?number_of_bathrooms__lt=number_of_bathrooms",
            "Search Property by Square Meters": "api/v1/properties?square_meters=square_meters",
            "Search Property by Square Meters Less than Equal": "api/v1/properties?square_meters__lte=square_meters",
            "Search Property by Square Meters Greater than Equal": "api/v1/properties?square_meters__gte=square_meters",
            "Search Property by Square Meters Less than": "api/v1/properties?square_meters__gt=square_meters",
            "Search Property by Square Meters Greater than": "api/v1/properties?square_meters__lt=square_meters",
            "Search Property by Parking Space": "api/v1/properties?parking_space=parking_space",
            "Search Property by Parking Space Less than Equal": "api/v1/properties?parking_space__lte=parking_space",
            "Search Property by Parking Space Greater than Equal": "api/v1/properties?parking_space__gte=parking_space",
            "Search Property by Parking Space Less than": "api/v1/properties?parking_space__gt=parking_space",
            "Search Property by Parking Space Greater than": "api/v1/properties?parking_space__lt=parking_space",
            "Search Property by City ID": "api/v1/properties?city=city_id",
            "Search Property by City Name": "api/v1/properties?city__name=city_name",
            "Search Property by Province": "api/v1/properties?province=province",
            "Search Property by Country Name": "api/v1/properties?country=country",
            "Search Property by Is Featured": "api/v1/properties?is_featured=is_featured",
            "Search Property by Listing Status ID": "api/v1/properties?listing_status=listing_status_id",
            "Search Property by Listing Status Name": "api/v1/properties?listing_status__name=listing_status_name",
            "Search Property by Category ID": "api/v1/properties?category=category_id",
            "Search Property by Category Name": "api/v1/properties?category__name=category_name"

        },
        status=status.HTTP_200_OK,
    )


class NewsletterAPIView(ListAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def get_view_name(self):
        return "Global Estate Hub Newsletters"

    def get_view_description(self, html=False):
        return "API view with all newsletters on the Global Estate Hub platform."
