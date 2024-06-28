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
            "Main": {
                "Newsletters": "api/v1/newsletters",
            },
            "Accounts": {
                "Users": {
                    "Registered Users": "api/v1/users",
                    "Registered User Details": "api/v1/users/<int:pk>",
                    "Registered Users by Account Type": "api/v1/users?account_type=<str:account_type>",
                    "Registered Users by Is Agent": "api/v1/users?is_agent=<bool:is_agent>",
                    "Registered Users by Is Verified": "api/v1/users?is_verified=<bool:is_verified>",
                },
                "Profiles": {
                    "Individual Profiles": "api/v1/users/individuals",
                    "Individual Profile Details": "api/v1/users/individuals/<int:pk>",
                    "Individual Profiles by Gender": "api/v1/users/individuals?gender=<str:gender>",
                    "Individual Profiles by Country": "api/v1/users/individuals?country=<str:country>",
                    "Individual Profiles by Province": "api/v1/users/individuals?province=<str:province>",
                    "Individual Profiles by City": "api/v1/users/individuals?city=<str:city>",
                    "Business Profiles": "api/v1/users/business",
                    "Business Profile Details": "api/v1/users/business/<int:pk>",
                    "Business Profiles by Country": "api/v1/users/business?country=<str:country>",
                    "Business Profiles by Province": "api/v1/users/business?province=<str:province>",
                    "Business Profiles by City": "api/v1/users/business?city=<str:city>",
                },
            },
            "Blog": {
                "Articles": {
                    "Articles": "api/v1/articles",
                    "Article Details": "api/v1/articles/<int:pk>",
                    "Articles by Category ID": "api/v1/articles?category__id=<int:pk>",
                    "Articles by Category Name": "api/v1/articles?category__name=<str:category.name>",
                },
                "Comments": {
                    "Comments": "api/v1/comments",
                    "Comment Details": "api/v1/comments/<int:pk>",
                    "Comments by User ID": "api/v1/comments?user__id=<int:user_id>",
                    "Comments by User Username": "api/v1/comments?user__username=<str:user_username>",
                    "Comments by Is Active": "api/v1/comments?active=<bool:is_active>",
                    "Comments by Level": "api/v1/comments?level=<int:level>",
                    "Article Comments by Article ID": "api/v1/comments?article__id=<int:article_id>",
                    "Article Comments by Article Title": "api/v1/comments?article__title=<str:article_title>",
                },
            },
            "Properties": {
                "Properties": {
                    "Properties": "api/v1/properties",
                    "Property Details": "api/v1/properties/<int:pk>",
                    "Properties by User ID": "api/v1/properties?user__id=<int:user_id>",
                    "Properties by User Username": "api/v1/properties?user__username=<str:user_username>",
                    "Properties by Listing Status ID": "api/v1/properties?listing_status=<int:listing_status_id>",
                    "Properties by Listing Status Name": "api/v1/properties?listing_status__name=<str:listing_status_name>",
                    "Properties by Category ID": "api/v1/properties?category=<int:category_id>",
                    "Properties by Category Name": "api/v1/properties?category__name=<str:category_name>",
                    "Properties by Year of Built": "api/v1/properties?year_of_built=<int:year_of_built>",
                    "Properties by Year of Built (LTE)": "api/v1/properties?year_of_built__lte=<int:year_of_built>",
                    "Properties by Year of Built (GTE)": "api/v1/properties?year_of_built__gte=<int:year_of_built>",
                    "Properties by Year of Built (LT)": "api/v1/properties?year_of_built__lt=<int:year_of_built>",
                    "Properties by Year of Built (GT)": "api/v1/properties?year_of_built__gt=<int:year_of_built>",
                    "Properties by Price": "api/v1/properties?price=<float:price>",
                    "Properties by Price (LTE)": "api/v1/properties?price__lte=<float:price>",
                    "Properties by Price (GTE)": "api/v1/properties?price__gte=<float:price>",
                    "Properties by Price (LT)": "api/v1/properties?price__lt=<float:price>",
                    "Properties by Price (GT)": "api/v1/properties?price__gt=<float:price>",
                    "Properties by Number of Bedrooms": "api/v1/properties?number_of_bedrooms=<int:number_of_bedrooms",
                    "Properties by Number of Bedrooms (LTE)": "api/v1/properties?number_of_bedrooms__lte=<int:number_of_bedrooms>",
                    "Properties by Number of Bedrooms (GTE)": "api/v1/properties?number_of_bedrooms__gte=<int:number_of_bedrooms>",
                    "Properties by Number of Bedrooms (LT)": "api/v1/properties?number_of_bedrooms__lt=<int:number_of_bedrooms>",
                    "Properties by Number of Bedrooms (GT)": "api/v1/properties?number_of_bedrooms__gt=<int:number_of_bedrooms>",
                    "Properties by Number of Bathrooms": "api/v1/properties?number_of_bathrooms=<int:number_of_bathrooms",
                    "Properties by Number of Bathrooms (LTE)": "api/v1/properties?number_of_bathrooms__lte=<int:number_of_bathrooms>",
                    "Properties by Number of Bathrooms (GTE)": "api/v1/properties?number_of_bathrooms__gte=<int:number_of_bathrooms>",
                    "Properties by Number of Bathrooms (LT)": "api/v1/properties?number_of_bathrooms__lt=<int:number_of_bathrooms>",
                    "Properties by Number of Bathrooms (GT)": "api/v1/properties?number_of_bathrooms__gt=<int:number_of_bathrooms>",
                    "Properties by Square Meters": "api/v1/properties?square_meters=<float:square_meters>",
                    "Properties by Square Meters (LTE)": "api/v1/properties?square_meters__lte=<float:square_meters>",
                    "Properties by Square Meters (GTE)": "api/v1/properties?square_meters__gte=<float:square_meters>",
                    "Properties by Square Meters (LT)": "api/v1/properties?square_meters__lt=<float:square_meters>",
                    "Properties by Square Meters (GT)": "api/v1/properties?square_meters__gt=<float:square_meters>",
                    "Properties by Parking Space": "api/v1/properties?parking_space=<int:parking_space>",
                    "Properties by Parking Space (LTE)": "api/v1/properties?parking_space__lte=<int:parking_space>",
                    "Properties by Parking Space (GTE)": "api/v1/properties?parking_space__gte=<int:parking_space>",
                    "Properties by Parking Space (LT)": "api/v1/properties?parking_space__lt=<int:parking_space>",
                    "Properties by Parking Space (GT)": "api/v1/properties?parking_space__gt=<int:parking_space>",
                    "Properties by City ID": "api/v1/properties?city=<int:city_id>",
                    "Properties by City Name": "api/v1/properties?city__name=<str:city_name>",
                    "Properties by Province": "api/v1/properties?province=<str:province>",
                    "Properties by Country": "api/v1/properties?country=<str:country>",
                    "Properties by Is Featured": "api/v1/properties?is_featured=<bool:is_featured>",
                },
                "Reviews": {
                    "Reviews": "api/v1/reviews",
                    "Review Details": "api/v1/reviews/<int:pk>",
                    "Reviews by User ID": "api/v1/reviews?user=<int:user_id>",
                    "Reviews by User Username": "api/v1/reviews?user__username=<str:user_username>",
                    "Reviews by Property ID": "api/v1/reviews?property=<int:property_id>",
                    "Reviews by Property Title": "api/v1/reviews?property__title=<str:property_title>",
                },
                "Tour Schedules": {
                    "Tour Schedules": "api/v1/tour-schedules",
                    "Tour Schedule Details": "api/v1/tour-schedules/<int:pk>",
                    "Tour Schedules by Customer ID": "api/v1/tour-schedules?customer=<int:customer_id>",
                    "Tour Schedules by Customer Username": "api/v1/tour-schedules?customer__username=<str:customer_username>",
                    "Tour Schedules by Property ID": "api/v1/tour-schedules?property=<int:property_id>",
                    "Tour Schedules by Property Title": "api/v1/tour-schedules?property__title=<str:property_title>",
                },
            },
        },
        status=status.HTTP_200_OK
    )


class NewsletterAPIView(ListAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def get_view_name(self):
        return "Global Estate Hub Newsletters"
