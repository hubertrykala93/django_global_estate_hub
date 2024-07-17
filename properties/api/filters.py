import django_filters
from properties.models import Property


class PropertyFilter(django_filters.FilterSet):
    category_id = django_filters.MultipleChoiceFilter(
        field_name="category__id",
        label="Category ID",
    )
    category_name = django_filters.MultipleChoiceFilter(
        field_name="category__name",
        label="Category Name",
    )
    min_year = django_filters.NumberFilter(
        field_name="year_of_built", lookup_expr="gte"
    )
    max_year = django_filters.NumberFilter(
        field_name="year_of_built", lookup_expr="lte"
    )
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_bedrooms = django_filters.NumberFilter(
        field_name="number_of_bedrooms", lookup_expr="gte"
    )
    max_bedrooms = django_filters.NumberFilter(
        field_name="number_of_bedrooms", lookup_expr="lte"
    )
    min_bathrooms = django_filters.NumberFilter(
        field_name="number_of_bathrooms", lookup_expr="gte"
    )
    max_bathrooms = django_filters.NumberFilter(
        field_name="number_of_bathrooms", lookup_expr="lte"
    )
    min_square = django_filters.NumberFilter(
        field_name="square_meters", lookup_expr="gte"
    )
    max_square = django_filters.NumberFilter(
        field_name="square_meters", lookup_expr="lte"
    )
    min_space = django_filters.NumberFilter(
        field_name="parking_space", lookup_expr="gte"
    )
    max_space = django_filters.NumberFilter(
        field_name="parking_space", lookup_expr="lte"
    )

    class Meta:
        model = Property
        fields = {
            "user__id": ["exact"],
            "user__username": ["exact"],
            "year_of_built": ["exact"],
            "price": ["exact"],
            "number_of_bedrooms": ["exact"],
            "number_of_bathrooms": ["exact"],
            "square_meters": ["exact"],
            "parking_space": ["exact"],
            "city__id": ["exact"],
            "city__name": ["exact"],
            "province": ["exact"],
            "country": ["exact"],
            "is_featured": ["exact"],
            "listing_status__id": ["exact"],
            "listing_status__name": ["exact"],
            "category__id": ["in"],
            "category__name": ["in"],
        }
