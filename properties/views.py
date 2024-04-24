import django.core.paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
import re
import os
from accounts.models import User, Individual, Business
from django.contrib import messages
from .models import (
    Property,
    ListingStatus,
    Category,
    City,
    Review,
    TourSchedule,
    Amenities,
    Img,
    Education,
    HealthAndMedical,
    Transportation,
    Shopping,
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from unidecode import unidecode
from datetime import datetime
from datetime import timedelta
from django.db.models import Min, Max
import requests
import uuid
from random import randint


def property_pagination(request, object_list, per_page) -> django.core.paginator.Page:
    """
    Returns Page object for pagination.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        object_list: django.db.models.query.Queryset
        per_page: int

    Returns
    ----------
        django.core.paginator.Page
    """
    paginator = Paginator(object_list=object_list, per_page=per_page)
    page = request.GET.get("page")
    pages = paginator.get_page(number=page)

    if page is None:
        pages = paginator.get_page(number=1)

    else:
        if page not in list(str(i) for i in pages.paginator.page_range):
            return redirect(to="error")

    return pages


def properties_context() -> dict:
    """
    Returns context for the properties page if the user is not using any filters.
    The values in filters such as Category, Rooms, Location, and Square Meters
    are narrowed down to the listing_status. In this case, to the 'Rent' status.

    Returns
    ----------
        dict
    """
    return {
        "listing_statuses": ListingStatus.objects.get_by_name(),
        "categories": Property.objects.filter(
            listing_status_id=ListingStatus.objects.get(name="Rent").id
        )
        .values_list("category__name", flat=True)
        .order_by("category__name")
        .distinct(),
        "number_of_bedrooms": [
            str(obj)
            for obj in Property.objects.filter(
                listing_status_id=ListingStatus.objects.get(name="Rent").id
            )
            .values_list("number_of_bedrooms", flat=True)
            .order_by("number_of_bedrooms")
            .distinct()
        ],
        "number_of_bathrooms": [
            str(obj)
            for obj in Property.objects.filter(
                listing_status_id=ListingStatus.objects.get(name="Rent").id
            )
            .values_list("number_of_bathrooms", flat=True)
            .order_by("number_of_bathrooms")
            .distinct()
        ],
        "cities": Property.objects.filter(
            listing_status_id=ListingStatus.objects.get(name="Rent").id
        )
        .values_list("city__name", flat=True)
        .order_by("city__name")
        .distinct(),
        "square_meters": [
            str(obj)
            for obj in Property.objects.filter(
                listing_status_id=ListingStatus.objects.get(name="Rent").id
            )
            .values_list("square_meters", flat=True)
            .order_by("square_meters")
            .distinct()
        ],
    }


def sidebar_context(**kwargs) -> dict:
    """
    Returns context for the properties page when the user is using filters.
    Values in filters such as Category and Location are narrowed down based on the user-selected Status,
    while values in filters such as Rooms and Square Meters are narrowed down to all user-selected filters.

    Parameters
    ----------
        kwargs: dict

    Returns
    ----------
        dict
    """
    return {
        "listing_statuses": ListingStatus.objects.get_by_name(),
        "categories": Property.objects.filter(
            listing_status_id=kwargs["listing_status_id"]
        )
        .values_list("category__name", flat=True)
        .order_by("category__name")
        .distinct(),
        "number_of_bedrooms": [
            str(obj)
            for obj in Property.objects.filter(**kwargs)
            .values_list("number_of_bedrooms", flat=True)
            .order_by("number_of_bedrooms")
            .distinct()
        ],
        "number_of_bathrooms": [
            str(obj)
            for obj in Property.objects.filter(**kwargs)
            .values_list("number_of_bathrooms", flat=True)
            .order_by("number_of_bathrooms")
            .distinct()
        ],
        "cities": Property.objects.filter(listing_status_id=kwargs["listing_status_id"])
        .values_list("city__name", flat=True)
        .order_by("city__name")
        .distinct(),
        "square_meters": [
            str(obj)
            for obj in Property.objects.filter(**kwargs)
            .values_list("square_meters", flat=True)
            .order_by("square_meters")
            .distinct()
        ],
    }


def properties(request) -> django.http.response.HttpResponse:
    """
    The function handles a GET request. It includes sorting properties by Newest Properties, Oldest Properties,
    Price (ascending), Price (descending), and Featured properties.
    The function also handles two forms using the GET method.
    The first form is for searching properties by keyword in the property title.
    The second form is for filtering properties, and after selecting each filter,
    the page reloads and displays the newly filtered properties.
    Keywords and filters are also stored in the session for further sorting.
    Pagination has also been implemented. Finally, the function returns an HttpResponse for the properties template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    queryset = []
    context = {}
    filters = {}
    checked_filters = {}

    if request.GET:
        if "properties-order" in request.GET:
            if "keyword" in request.session:
                if request.session.get("filters"):
                    request.session.pop("filters")

                if request.session.get("checked_filters"):
                    request.session.pop("checked_filters")

                context.update(properties_context())

                if "Newest Properties" in request.GET.get("properties-order"):
                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(
                        Property.objects.get_by_keyword(
                            keyword=request.session["keyword"], order_by="-date_posted"
                        )
                    )

                elif "Oldest Properties" in request.GET.get("properties-order"):
                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(
                        Property.objects.get_by_keyword(
                            keyword=request.session["keyword"], order_by="date_posted"
                        )
                    )

                elif "Price Ascending" in request.GET.get("properties-order"):
                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(
                        Property.objects.get_by_keyword(
                            keyword=request.session["keyword"], order_by="price"
                        )
                    )

                elif "Price Descending" in request.GET.get("properties-order"):
                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(
                        Property.objects.get_by_keyword(
                            keyword=request.session["keyword"], order_by="-price"
                        )
                    )

                elif "Featured" in request.GET.get("properties-order"):
                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(
                        Property.objects.get_by_keyword(
                            keyword=request.session["keyword"], order_by="-is_featured"
                        )
                    )

                else:
                    request.session["sorted_type"] = "Newest Properties"
                    queryset.extend(
                        Property.objects.get_by_keyword(
                            keyword=request.session["keyword"], order_by="-date_posted"
                        )
                    )

            elif "filters" in request.session:
                context.update(sidebar_context(**request.session["filters"]))

                if "Newest Properties" in request.GET.get("properties-order"):
                    if request.session.get("filters").get("is_featured"):
                        request.session.get("filters").pop("is_featured")

                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(
                        Property.objects.get_by_filters(
                            "-date_posted", **request.session["filters"]
                        )
                    )

                elif "Oldest Properties" in request.GET.get("properties-order"):
                    if request.session.get("filters").get("is_featured"):
                        request.session.get("filters").pop("is_featured")

                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(
                        Property.objects.get_by_filters(
                            "date_posted", **request.session["filters"]
                        )
                    )

                elif "Price Ascending" in request.GET.get("properties-order"):
                    if request.session.get("filters").get("is_featured"):
                        request.session.get("filters").pop("is_featured")

                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(
                        Property.objects.get_by_filters(
                            "price", **request.session["filters"]
                        )
                    )

                elif "Price Descending" in request.GET.get("properties-order"):
                    if request.session.get("filters").get("is_featured"):
                        request.session.get("filters").pop("is_featured")

                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(
                        Property.objects.get_by_filters(
                            "-price", **request.session["filters"]
                        )
                    )

                elif "Featured" in request.GET.get("properties-order"):
                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(
                        Property.objects.get_by_filters(
                            "-is_featured", **request.session["filters"]
                        )
                    )

                else:
                    if request.session.get("filters").get("is_featured"):
                        request.session.get("filters").pop("is_featured")

                    request.session["sorted_type"] = "Newest Properties"
                    queryset.extend(
                        Property.objects.get_by_filters(
                            "-date_posted", **request.session["filters"]
                        )
                    )

            else:
                context.update(properties_context())

                if "Newest Properties" in request.GET.get("properties-order"):
                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(Property.objects.all().order_by("-date_posted"))

                elif "Oldest Properties" in request.GET.get("properties-order"):
                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(Property.objects.all().order_by("date_posted"))

                elif "Price Ascending" in request.GET.get("properties-order"):
                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(Property.objects.all().order_by("price"))

                elif "Price Descending" in request.GET.get("properties-order"):
                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(Property.objects.all().order_by("-price"))

                elif "Featured" in request.GET.get("properties-order"):
                    request.session["sorted_type"] = request.GET.get("properties-order")
                    queryset.extend(Property.objects.all().order_by("-is_featured"))

                else:
                    request.session["sorted_type"] = "Newest Properties"
                    queryset.extend(Property.objects.all().order_by("-date_posted"))

        elif "keyword" in request.GET:
            if request.session.get("checked_filters"):
                request.session.pop("checked_filters")

            context.update(properties_context())

            request.session["sorted_type"] = "Newest Properties"
            request.session["keyword"] = request.GET.get("keyword")
            queryset.extend(
                Property.objects.get_by_keyword(
                    keyword=request.GET.get("keyword"), order_by="-date_posted"
                )
            )

        elif (
                "status" in request.GET
                or "category" in request.GET
                or "min_price" in request.GET
                or "max_price" in request.GET
                or "min_bedrooms" in request.GET
                or "max_bedrooms" in request.GET
                or "min_bathrooms" in request.GET
                or "max_bathrooms" in request.GET
                or "location" in request.GET
                or "min_square" in request.GET
                or "max_square" in request.GET
        ):

            if request.session.get("keyword"):
                request.session.pop("keyword")

            if "status" in request.GET:
                filters["listing_status_id"] = ListingStatus.objects.get(
                    slug="-".join(request.GET.get("status").lower().split())
                ).id

                if len(Property.objects.filter(**filters)) == 0:
                    queryset.clear()

                request.session["sorted_type"] = "Newest Properties"
                request.session["filters"] = filters
                checked_filters.update(
                    {
                        "checked_status": request.GET.get("status").capitalize(),
                    }
                )
                request.session["checked_filters"] = checked_filters

                context.update(sidebar_context(**filters))
                queryset.extend(
                    Property.objects.filter(**filters).order_by("-date_posted")
                )

            if "category" in request.GET:
                filters["category__pk__in"] = [
                    Category.objects.get(slug="-".join(obj.lower().split())).id
                    for obj in request.GET.getlist("category")
                ]

                if len(Property.objects.filter(**filters)) == 0:
                    queryset.clear()

                else:
                    checked_categories = request.GET.getlist("category")
                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_categories": [
                                category.capitalize()
                                for category in request.GET.getlist("category")
                            ],
                        }
                    )
                    request.session["checked_filters"] = checked_filters

                    context.update(
                        {
                            "checked_categories": checked_categories,
                        }
                    )
                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

            if "min_bedrooms" in request.GET:
                if "max_bedrooms" in request.GET:
                    filters["number_of_bedrooms__range"] = [
                        int(request.GET.get("min_bedrooms")),
                        int(request.GET.get("max_bedrooms")),
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_min_bedrooms": request.GET.get("min_bedrooms"),
                            "checked_max_bedrooms": request.GET.get("max_bedrooms"),
                        }
                    )
                    request.session["checked_filters"] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

                else:
                    filters["number_of_bedrooms__range"] = [
                        int(request.GET.get("min_bedrooms")),
                        Property.objects.aggregate(Max("number_of_bedrooms"))[
                            "number_of_bedrooms__max"
                        ],
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_min_bedrooms": request.GET.get("min_bedrooms"),
                        }
                    )
                    request.session["checked_filters"] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

            if "max_bedrooms" in request.GET:

                if "min_bedrooms" in request.GET:
                    filters["number_of_bedrooms__range"] = [
                        int(request.GET.get("min_bedrooms")),
                        int(request.GET.get("max_bedrooms")),
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_min_bedrooms": request.GET.get("min_bedrooms"),
                            "checked_max_bedrooms": request.GET.get("max_bedrooms"),
                        }
                    )
                    request.session["checked_filters"] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

                else:
                    filters["number_of_bedrooms__range"] = [
                        Property.objects.aggregate(Min("number_of_bedrooms"))[
                            "number_of_bedrooms__min"
                        ],
                        int(request.GET.get("max_bedrooms")),
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_max_bedrooms": request.GET.get("max_bedrooms"),
                        }
                    )

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

            if "min_bathrooms" in request.GET:
                if "max_bathrooms" in request.GET:
                    filters["number_of_bathrooms__range"] = [
                        int(request.GET.get("min_bathrooms")),
                        int(request.GET.get("max_bathrooms")),
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_min_bathrooms": request.GET.get("min_bathrooms"),
                            "checked_max_bathrooms": request.GET.get("max_bathrooms"),
                        }
                    )
                    request.session["checked_filters"] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

                else:
                    filters["number_of_bathrooms__range"] = [
                        int(request.GET.get("min_bathrooms")),
                        Property.objects.aggregate(Max("number_of_bathrooms"))[
                            "number_of_bathrooms__max"
                        ],
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_min_bathrooms": request.GET.get("min_bathrooms"),
                        }
                    )
                    request.session["checked_filters"] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

            if "max_bathrooms" in request.GET:
                if "min_bathrooms" in request.GET:
                    filters["number_of_bathrooms__range"] = [
                        int(request.GET.get("min_bathrooms")),
                        int(request.GET.get("max_bathrooms")),
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_min_bathrooms": request.GET.get("min_bathrooms"),
                            "checked_max_bathrooms": request.GET.get("max_bathrooms"),
                        }
                    )
                    request.session["checked_filters"] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

                else:
                    filters["number_of_bathrooms__range"] = [
                        Property.objects.aggregate(Min("number_of_bathrooms"))[
                            "number_of_bathrooms__min"
                        ],
                        int(request.GET.get("max_bathrooms")),
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_max_bathrooms": request.GET.get("max_bathrooms"),
                        }
                    )
                    request.session["checked_filters"] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

            if "location" in request.GET:
                filters["city__id"] = City.objects.get(
                    slug=unidecode(
                        "-".join(request.GET.get("location").lower().split())
                    )
                ).id

                if len(Property.objects.filter(**filters)) == 0:
                    queryset.clear()

                request.session["sorted_type"] = "Newest Properties"
                request.session["filters"] = filters
                checked_filters.update(
                    {
                        "city": request.GET.get("location").capitalize(),
                    }
                )
                request.session["checked_filters"] = checked_filters

                context.update(sidebar_context(**filters))

                queryset.clear()
                queryset.extend(
                    Property.objects.filter(**filters).order_by("-date_posted")
                )

            if "min_square" in request.GET:
                if "max_square" in request.GET:
                    filters["square_meters__range"] = [
                        float(request.GET.get("min_square")),
                        float(request.GET.get("max_square")),
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_min_square": request.GET.get("min_square"),
                            "checked_max_square": request.GET.get("max_square"),
                        }
                    )
                    request.session["checked_filters"] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

                else:
                    filters["square_meters__range"] = [
                        float(request.GET.get("min_square")),
                        Property.objects.aggregate(Max("square_meters"))[
                            "square_meters__max"
                        ],
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_min_square": request.GET.get("min_square"),
                        }
                    )
                    request.session["checked_filters"] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

            if "max_square" in request.GET:
                if "min_square" in request.GET:
                    filters["square_meters__range"] = [
                        float(request.GET.get("min_square")),
                        float(request.GET.get("max_square")),
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_min_square": request.GET.get("min_square"),
                            "checked_max_square": request.GET.get("max_square"),
                        }
                    )
                    request.session["checked_filters"] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

                else:
                    filters["square_meters__range"] = [
                        Property.objects.aggregate(Min("square_meters"))[
                            "square_meters__min"
                        ],
                        float(request.GET.get("max_square")),
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session["sorted_type"] = "Newest Properties"
                    request.session["filters"] = filters
                    checked_filters.update(
                        {
                            "checked_max_square": request.GET.get("max_square"),
                        }
                    )
                    request.session["checked_filters"] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(
                        Property.objects.filter(**filters).order_by("-date_posted")
                    )

        else:
            context.update(properties_context())

            if request.session.get("sorted_type"):
                request.session.pop("sorted_type")

            request.session["sorted_type"] = "Newest Properties"
            queryset.extend(Property.objects.all().order_by("-date_posted"))

    else:
        # if request.session.get("new_property"):
        #     request.session.pop("new_property")

        if request.session.get("country_code"):
            request.session.pop("country_code")

        if request.session.get("province_code"):
            request.session.pop("province_code")

        if request.session.get("sorted_type"):
            request.session.pop("sorted_type")

        if request.session.get("keyword"):
            request.session.pop("keyword")

        if request.session.get("filters"):
            request.session.pop("filters")

        if request.session.get("checked_filters"):
            request.session.pop("checked_filters")

        request.session["sorted_type"] = "Newest Properties"
        queryset.extend(Property.objects.all().order_by("-date_posted"))

        context.update(properties_context())

    context.update(
        {
            "title": "Properties",
            "properties": len(queryset),
            "sorted_type": request.session["sorted_type"],
            "pages": property_pagination(
                request=request, object_list=queryset, per_page=6
            ),
        }
    )

    return render(
        request=request, template_name="properties/properties.html", context=context
    )


def property_categories(request, category_slug) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the property-categories template along with pagination.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        category_slug: str

    Returns
    ----------
        django.http.response.HttpResponse
    """
    category = get_object_or_404(klass=Category, slug=category_slug)

    queryset = []

    if request.GET:
        if "properties-order" in request.GET:
            if "Newest Properties" in request.GET.get("properties-order"):
                request.session["sorted_type"] = request.GET.get("properties-order")
                queryset.extend(
                    Property.objects.filter(category=category).order_by("-date_posted")
                )

            elif "Oldest Properties" in request.GET.get("properties-order"):
                request.session["sorted_type"] = request.GET.get("properties-order")
                queryset.extend(
                    Property.objects.filter(category=category).order_by("date_posted")
                )

            elif "Price Ascending" in request.GET.get("properties-order"):
                request.session["sorted_type"] = request.GET.get("properties-order")
                queryset.extend(
                    Property.objects.filter(category=category).order_by("price")
                )

            elif "Price Descending" in request.GET.get("properties-order"):
                request.session["sorted_type"] = request.GET.get("properties-order")
                queryset.extend(
                    Property.objects.filter(category=category).order_by("-price")
                )

            elif "Featured" in request.GET.get("properties-order"):
                request.session["sorted_type"] = request.GET.get("properties-order")
                queryset.extend(
                    Property.objects.filter(category=category).order_by("-is_featured")
                )

            else:
                request.session["sorted_type"] = "Newest Properties"
                queryset.extend(
                    Property.objects.filter(category=category).order_by("-date_posted")
                )

        else:
            if request.session.get("sorted_type"):
                request.session.pop("sorted_type")

            request.session["sorted_type"] = "Newest Properties"
            queryset.extend(
                Property.objects.filter(category=category).order_by("-date_posted")
            )

    else:
        if request.session.get("sorted_type"):
            request.session.pop("sorted_type")

        request.session["sorted_type"] = "Newest Properties"
        queryset.extend(
            Property.objects.filter(category=category).order_by("-date_posted")
        )

    return render(
        request=request,
        template_name="properties/properties-category.html",
        context={
            "title": f"{category} Properties",
            "category": category,
            "properties": queryset,
            "sorted_type": request.session["sorted_type"],
            "pages": property_pagination(
                request=request, object_list=queryset, per_page=6
            ),
        },
    )


def property_cities(request, city_slug) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the property-cities template along with pagination.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        city_slug: str

    Returns
    ----------
        django.http.response.HttpResponse
    """
    city = get_object_or_404(klass=City, slug=city_slug)
    queryset = []

    if request.GET:
        if "properties-order" in request.GET:
            if "Newest Properties" in request.GET.get("properties-order"):
                request.session["sorted_type"] = request.GET.get("properties-order")
                queryset.extend(
                    Property.objects.filter(city=city).order_by("-date_posted")
                )

            elif "Oldest Properties" in request.GET.get("properties-order"):
                request.session["sorted_type"] = request.GET.get("properties-order")
                queryset.extend(
                    Property.objects.filter(city=city).order_by("date_posted")
                )

            elif "Price Ascending" in request.GET.get("properties-order"):
                request.session["sorted_type"] = request.GET.get("properties-order")
                queryset.extend(Property.objects.filter(city=city).order_by("price"))

            elif "Price Descending" in request.GET.get("properties-order"):
                request.session["sorted_type"] = request.GET.get("properties-order")
                queryset.extend(Property.objects.filter(city=city).order_by("-price"))

            elif "Featured" in request.GET.get("properties-order"):
                request.session["sorted_type"] = request.GET.get("properties-order")
                queryset.extend(
                    Property.objects.filter(city=city).order_by("-is_featured")
                )

            else:
                request.session["sorted_type"] = "Newest Properties"
                queryset.extend(
                    Property.objects.filter(city=city).order_by("-date_posted")
                )

        else:
            if request.session.get("sorted_type"):
                request.session.pop("sorted_type")

            request.session["sorted_type"] = "Newest Properties"
            queryset.extend(Property.objects.filter(city=city).order_by("-date_posted"))

    else:
        if request.session.get("sorted_type"):
            request.session.pop("sorted_type")

        request.session["sorted_type"] = "Newest Properties"
        queryset.extend(Property.objects.filter(city=city).order_by("-date_posted"))

    return render(
        request=request,
        template_name="properties/properties-cities.html",
        context={
            "title": f"{city} Properties",
            "city": city,
            "properties": queryset,
            "sorted_type": request.session["sorted_type"],
            "pages": property_pagination(
                request=request, object_list=queryset, per_page=6
            ),
        },
    )


@login_required(login_url="login")
def add_property(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the add-property template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    country_response = requests.request(
        method="GET",
        url="https://api.countrystatecity.in/v1/countries",
        headers={
            "X-CSCAPI-KEY": "T05jNG1pSjlhZnE3SWM3c0RLcVpNV2NBTWJKVWFhcVZFWVZ4VE9zaQ=="
        },
    )

    countries = sorted(
        [
            {
                "name": country.title(),
                "slug": "-".join(
                    country.lower().replace("(", "").replace(")", "").split()
                ),
            }
            for country in [unidecode(data["name"]) for data in country_response.json()]
        ],
        key=lambda d: d["name"],
    )

    return render(
        request=request,
        template_name="properties/add-property.html",
        context={
            "title": "Add Property",
            "categories": Category.objects.all().order_by("name"),
            "amenities": Amenities.objects.all().order_by("name"),
            "countries": countries,
        },
    )


def set_location(request):
    if request.method == "POST":
        if request.session.get("country_code"):
            request.session.pop("country_code")

        if request.session.get("province_code"):
            request.session.pop("province_code")

        data = json.loads(s=request.body.decode(encoding="utf-8"))

        country_response = requests.request(
            method="GET",
            url="https://api.countrystatecity.in/v1/countries",
            headers={
                "X-CSCAPI-KEY": "T05jNG1pSjlhZnE3SWM3c0RLcVpNV2NBTWJKVWFhcVZFWVZ4VE9zaQ=="
            },
        )

        country_code = [
            d["iso2"]
            for d in country_response.json()
            if d["name"].title() == data["country"]
        ][0]
        request.session["country_code"] = country_code

        # provinces by country
        province_response = requests.request(
            method="GET",
            url=f"https://api.countrystatecity.in/v1/countries/{country_code}/states",
            headers={
                "X-CSCAPI-KEY": "T05jNG1pSjlhZnE3SWM3c0RLcVpNV2NBTWJKVWFhcVZFWVZ4VE9zaQ==",
            },
        )

        # cities by country
        cities_response = requests.request(
            method="GET",
            url=f"https://api.countrystatecity.in/v1/countries/{country_code}/cities",
            headers={
                "X-CSCAPI-KEY": "T05jNG1pSjlhZnE3SWM3c0RLcVpNV2NBTWJKVWFhcVZFWVZ4VE9zaQ==",
            },
        )

        unique_provinces = set(
            [unidecode(d["name"].title()) for d in province_response.json()]
        )

        provinces = sorted(
            [
                {
                    "name": province.replace("'", ""),
                    "slug": "-".join(
                        province.lower()
                        .replace("(", "")
                        .replace(")", "")
                        .replace("`", "")
                        .replace("'", "")
                        .split()
                    ),
                }
                for province in unique_provinces
            ],
            key=lambda d: d["name"],
        )

        if data["province"] is False:
            unique_cities = list(
                set([unidecode(d["name"].title()) for d in cities_response.json()])
            )

            cities = sorted(
                [
                    {
                        "name": city.replace("'", ""),
                        "slug": "-".join(
                            city.lower()
                            .replace("(", "")
                            .replace(")", "")
                            .replace("`", "")
                            .replace("'", "")
                            .split()
                        ),
                    }
                    for city in unique_cities
                ],
                key=lambda d: d["name"],
            )

            return JsonResponse(
                data={
                    "provinces": provinces,
                    "cities": cities,
                }
            )

        else:
            province_code = [
                d["iso2"]
                for d in province_response.json()
                if unidecode(d["name"]).title() == data["province"]
            ][0]

            request.session["province_code"] = province_code

            # cities by country and province
            province_response_by_country_and_province = requests.request(
                method="GET",
                url=f"https://api.countrystatecity.in/v1/countries/{country_code}/states/{province_code}/cities",
                headers={
                    "X-CSCAPI-KEY": "T05jNG1pSjlhZnE3SWM3c0RLcVpNV2NBTWJKVWFhcVZFWVZ4VE9zaQ==",
                },
            )

            unique_cities = list(
                set(
                    [
                        unidecode(d["name"].title())
                        for d in province_response_by_country_and_province.json()
                    ]
                )
            )

            cities = sorted(
                [
                    {
                        "name": city.replace("'", ""),
                        "slug": "-".join(
                            city.lower()
                            .replace("(", "")
                            .replace(")", "")
                            .replace("`", "")
                            .replace("'", "")
                            .split()
                        ),
                    }
                    for city in unique_cities
                ],
                key=lambda d: d["name"],
            )

            return JsonResponse(
                data={
                    "provinces": provinces,
                    "cities": cities,
                }
            )


def save_data_to_model():
    pass


def create_property(request):
    response = {}
    if request.method == "POST":
        spam_verification = request.POST["url"]
        title = request.POST["title"].strip()
        price = request.POST["price"].strip()
        description = request.POST["description"].strip()
        year_of_built = request.POST["year_of_built"].strip()
        number_of_bedrooms = request.POST["number_of_bedrooms"].strip()
        number_of_bathrooms = request.POST["number_of_bathrooms"].strip()
        square_meters = request.POST["square_meters"].strip()
        parking_space = request.POST["parking_space"].strip()
        postal_code = request.POST["postal_code"].strip()

        if len(spam_verification) != 0:
            return JsonResponse(
                data={
                    "valid": None,
                },
                safe=False,
            )

        # title
        response.update(
            {
                "title": {
                    "valid": (
                        False if not title else
                        False if len(title) < 10 else
                        False if len(title) > 100 else
                        False if Property.objects.filter(title=title).exists() else
                        True
                    ),
                    "message": (
                        "The 'title' field is required."
                        if not title
                        else (
                            "The title must consist of at least 10 characters."
                            if len(title) < 10
                            else (
                                "The title must consist of no more than 100 characters."
                                if len(title) > 100
                                else "An offer with this name already exists." if Property.objects.filter(
                                    title=title).exists() else ""
                            )
                        )
                    ),
                }
            }
        )

        # price
        response.update(
            {
                "price": {
                    "valid": (
                        False
                        if not price
                        else (
                            False
                            if price[0] != "-" and not price.isdigit()
                            else (
                                False
                                if price[0] == "-"
                                   and not price.isdigit()
                                   and price[1:].isdigit()
                                else (
                                    False
                                    if len(price) == 1
                                       and price.isdigit()
                                       and price == "0"
                                    else (
                                        False
                                        if len(price) > 1
                                           and price.isdigit()
                                           and price[0] == "0"
                                        else True
                                    )
                                )
                            )
                        )
                    ),
                    "message": (
                        "The 'price' field is required."
                        if not price
                        else (
                            "The price must be a number."
                            if price[0] != "-" and not price.isdigit()
                            else (
                                "The price must be greater than 0."
                                if price[0] == "-"
                                   and not price.isdigit()
                                   and price[1:].isdigit()
                                else (
                                    "The price must be greater than 0."
                                    if len(price) == 1
                                       and price.isdigit()
                                       and price == "0"
                                    else (
                                        "The price cannot start with 0."
                                        if len(price) > 1
                                           and price.isdigit()
                                           and price[0] == "0"
                                        else ""
                                    )
                                )
                            )
                        )
                    ),
                }
            }
        )

        # description
        response.update(
            {
                "description": {
                    "valid": False if not description else True,
                    "message": (
                        "The 'description' field is required."
                        if not description
                        else ""
                    ),
                }
            }
        )

        # year of built
        response.update(
            {
                "year_of_built": {
                    "valid": (
                        False
                        if not year_of_built
                        else (
                            False
                            if len(year_of_built) != 4 and not year_of_built.isdigit()
                            else (
                                False
                                if len(year_of_built) != 4 and year_of_built.isdigit()
                                else (
                                    False
                                    if len(year_of_built) == 4
                                       and not year_of_built.isdigit()
                                    else (
                                        False
                                        if len(year_of_built) != 4
                                           and year_of_built[0] == "-"
                                           and year_of_built[1:].isdigit()
                                        else (
                                            False
                                            if len(year_of_built) == 4
                                               and year_of_built[0] == "0"
                                               and year_of_built[1:].isdigit()
                                            else (
                                                False
                                                if datetime.now().year
                                                   < datetime.strptime(
                                                    year_of_built, "%Y"
                                                ).year
                                                else True
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    "message": (
                        "The 'year of built' field is required."
                        if not year_of_built
                        else (
                            "The actual year of built is required, and the year of built should consist solely of digits."
                            if len(year_of_built) != 4 and not year_of_built.isdigit()
                            else (
                                "The actual year of built is required."
                                if len(year_of_built) != 4 and year_of_built.isdigit()
                                else (
                                    "The year of built must consist of digits."
                                    if len(year_of_built) == 4
                                       and not year_of_built.isdigit()
                                    else (
                                        "The year of built cannot start with 0."
                                        if len(year_of_built) == 4
                                           and year_of_built[0] == "0"
                                           and year_of_built[1:].isdigit()
                                        else (
                                            "The year of built cannot be greater than actual year."
                                            if datetime.now().year
                                               < datetime.strptime(
                                                year_of_built, "%Y"
                                            ).year
                                            else ""
                                        )
                                    )
                                )
                            )
                        )
                    ),
                }
            }
        )

        # number of bedrooms
        response.update(
            {
                "number_of_bedrooms": {
                    "valid": (
                        False
                        if not number_of_bedrooms
                        else (
                            False
                            if number_of_bedrooms[0] == "-"
                               and number_of_bedrooms[1:].isdecimal()
                            else False if not number_of_bedrooms.isdecimal() else True
                        )
                    ),
                    "message": (
                        "The 'number of bedrooms' field is required."
                        if not number_of_bedrooms
                        else (
                            "The number of bedrooms must be greater than or equal 0."
                            if number_of_bedrooms[0] == "-"
                               and number_of_bedrooms[1:].isdecimal()
                            else (
                                "The number of bedrooms must consist of positive digits."
                                if not number_of_bedrooms.isdecimal()
                                else ""
                            )
                        )
                    ),
                }
            }
        )

        # number of bathrooms
        response.update(
            {
                "number_of_bathrooms": {
                    "valid": (
                        False
                        if not number_of_bathrooms
                        else (
                            False
                            if number_of_bathrooms[0] == "-"
                               and number_of_bathrooms[1:].isdecimal()
                            else False if not number_of_bathrooms.isdecimal() else True
                        )
                    ),
                    "message": (
                        "The 'number of bathrooms' field is required."
                        if not number_of_bedrooms
                        else (
                            "The number of bathrooms must be greater than or equal 0."
                            if number_of_bathrooms[0] == "-"
                               and number_of_bathrooms[1:].isdecimal()
                            else (
                                "The number of bathrooms must consist of positive digits."
                                if not number_of_bathrooms.isdecimal()
                                else ""
                            )
                        )
                    ),
                }
            }
        )

        # square meters
        response.update(
            {
                "square_meters": {
                    "valid": (
                        False
                        if not square_meters
                        else (
                            False
                            if square_meters[0] == "-" and square_meters[1:].isdecimal()
                            else (
                                False
                                if square_meters[0] == "-"
                                   and not square_meters[1:].isdecimal()
                                else (
                                    False
                                    if square_meters == "0"
                                    else (
                                        False
                                        if "," in square_meters
                                           and not square_meters.replace(",", "").isdigit()
                                        else (
                                            True
                                            if "," in square_meters
                                               and square_meters.replace(",", "").isdigit()
                                            else True
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    "message": (
                        "The 'square meters' field is required."
                        if not square_meters
                        else (
                            "Square meters must be greater than 0."
                            if square_meters[0] == "-" and square_meters[1:].isdecimal()
                            else (
                                "Square meters must consist of positive digits."
                                if square_meters[0] == "-"
                                   and not square_meters[1:].isdecimal()
                                else (
                                    "Square meters must be greater than 0."
                                    if square_meters == "0"
                                    else (
                                        "Square meters must consist of positive digits."
                                        if "," in square_meters
                                           and not square_meters.replace(",", "").isdigit()
                                        else (
                                            ""
                                            if "," in square_meters
                                               and square_meters.replace(",", "").isdigit()
                                            else ""
                                        )
                                    )
                                )
                            )
                        )
                    ),
                }
            }
        )

        # parking space
        response.update(
            {
                "parking_space": {
                    "valid": (
                        False
                        if not parking_space
                        else (
                            False
                            if not parking_space.isdigit()
                            else (
                                False
                                if parking_space[0] == "-"
                                   and parking_space[1:].isdigit()
                                else True if parking_space == "0" else True
                            )
                        )
                    ),
                    "message": (
                        "The 'parking space' field is required."
                        if not parking_space
                        else (
                            "Parking space must consist of positive digits."
                            if not parking_space.isdigit()
                            else (
                                "Parking space must be greater than or equal 0."
                                if parking_space[0] == "-"
                                   and parking_space[1:].isdigit()
                                else "" if parking_space == "0" else ""
                            )
                        )
                    ),
                }
            }
        )

        # status
        response.update(
            {
                "status": {
                    "valid": True if request.POST.get("status") else False,
                    "message": (
                        ""
                        if request.POST.get("status")
                        else "Status is required."
                    ),
                }
            }
        )

        # category
        response.update(
            {
                "category": {
                    "valid": True if request.POST.get("category") else False,
                    "message": (
                        ""
                        if request.POST.get("category")
                        else "Category is required."
                    ),
                }
            }
        )

        # country
        response.update(
            {
                "country": {
                    "valid": True if request.POST.get("country") else False,
                    "message": (
                        ""
                        if request.POST.get("country")
                        else "Country is required."
                    ),
                }
            }
        )

        # postal code
        response.update(
            {
                "postal_code": {
                    "valid": False if not postal_code else True,
                    "message": (
                        "The 'postal code' field is required."
                        if not postal_code
                        else ""
                    ),
                }
            }
        )

        # amenities
        response.update(
            {
                "amenities": {
                    "valid":
                        False if len(request.POST.getlist("amenities")) == 0 else
                        True,
                    "message":
                        "Amenities are required." if len(request.POST.getlist("amenities")) == 0 else
                        "",
                }
            }
        )

        if request.FILES:
            if "thumbnail" in request.FILES:
                response.update(
                    {
                        "thumbnail": {
                            "valid": (
                                False
                                if "thumbnail" in request.FILES
                                   and request.FILES.get("thumbnail").size > 1000000
                                else (
                                    False
                                    if "thumbnail" in request.FILES
                                       and request.FILES.get("thumbnail").size <= 1000000
                                       and request.FILES.get("thumbnail").name.split(
                                        sep="."
                                    )[1]
                                       not in ["jpg", "jpeg", "webp", "png", "svg"]
                                    else True
                                )
                            ),
                            "message": (
                                "The thumbnail size cannot exceed 1 MB."
                                if "thumbnail" in request.FILES
                                   and request.FILES.get("thumbnail").size > 1000000
                                else (
                                    "The thumbnail must be in JPG, JPEG, SVG, PNG, or WEBP format."
                                    if "thumbnail" in request.FILES
                                       and request.FILES.get("thumbnail").size <= 1000000
                                       and request.FILES.get("thumbnail").name.split(
                                        sep="."
                                    )[1]
                                       not in ["jpg", "jpeg", "webp", "png", "svg"]
                                    else ""
                                )
                            ),
                        }
                    }
                )

            else:
                response.update(
                    {
                        "thumbnail": {
                            "valid": False,
                            "message": "A thumbnail is required.",
                        }
                    }
                )

            if "gallery" in request.FILES:
                result = []

                for image in request.FILES.getlist("gallery"):
                    if image.size > 1000000 or image.name.split(sep=".")[1] not in [
                        "jpg",
                        "jpeg",
                        "webp",
                        "png",
                        "svg",
                    ]:
                        result.append(False)

                    else:
                        result.append(True)

                if len(set(result)) == 1 and result[0] is True:
                    response.update(
                        {
                            "gallery": {
                                "valid": True,
                                "message": "",
                            }
                        }
                    )

                else:
                    response.update(
                        {
                            "gallery": {
                                "valid": False,
                                "message": "The size of the photos cannot exceed 1 MB, and the photos must be in JPG, JPEG, PNG, SVG, or WEBP format.",
                            }
                        }
                    )

            else:
                response.update(
                    {
                        "gallery": {
                            "valid": False,
                            "message": "The photo gallery is required.",
                        }
                    }
                )

            if "video" in request.FILES:
                response.update(
                    {
                        "video": {
                            "valid": (
                                False
                                if "video" in request.FILES
                                   and request.FILES.get("video").size > 5000000
                                else (
                                    False
                                    if "video" in request.FILES
                                       and request.FILES.get("video").size <= 5000000
                                       and request.FILES.get("video").name.split(sep=".")[
                                           1
                                       ]
                                       != "mp4"
                                    else True
                                )
                            ),
                            "message": (
                                "The video size cannot exceed 5 MB."
                                if "video" in request.FILES
                                   and request.FILES.get("video").size > 5000000
                                else (
                                    "The video must be in MP4 format."
                                    if "video" in request.FILES
                                       and request.FILES.get("video").size <= 5000000
                                       and request.FILES.get("video").name.split(sep=".")[
                                           1
                                       ]
                                       != "mp4"
                                    else ""
                                )
                            ),
                        }
                    }
                )

            else:
                response.update(
                    {
                        "video": {
                            "valid": False,
                            "message": "Video is required.",
                        }
                    }
                )

        else:
            response.update(
                {
                    "thumbnail": {
                        "valid": False,
                        "message": "A thumbnail is required.",
                    },
                    "gallery": {
                        "valid": False,
                        "message": "The photo gallery is required.",
                    },
                    "video": {
                        "valid": False,
                        "message": "Video is required.",
                    },
                }
            )

        # education, health and medical, transportation, shopping
        nearbies = ["education", "health", "transportation", "shopping"]
        temporary_folders = [[], [], [], []]
        names = ["education", "health_and_medical", "transportation", "shopping"]

        for nearby, folder, name in zip(nearbies, temporary_folders, names):
            if (
                    len(request.POST.getlist(f"{nearby}-name")) == 1
                    and request.POST.getlist(f"{nearby}-name")[0] != ""
            ) or (
                    len(request.POST.getlist(f"{nearby}-distance")) == 1
                    and request.POST.getlist(f"{nearby}-distance")[0] != ""
            ):
                folder.append(
                    {
                        f"{nearby}_name": {
                            "valid": (
                                False
                                if request.POST.get(f"{nearby}-distance").strip()
                                   and not request.POST.get(f"{nearby}-name").strip()
                                else (
                                    False
                                    if request.POST.get(f"{nearby}-name").strip()
                                       and len(request.POST.get(f"{nearby}-name").strip()) <= 5
                                    else True
                                )
                            ),
                            "message": (
                                "If you have provided a distance, you must also provide a name."
                                if request.POST.get(f"{nearby}-distance").strip()
                                   and not request.POST.get(f"{nearby}-name").strip()
                                else (
                                    "The name must be at least 5 characters long."
                                    if request.POST.get(f"{nearby}-name").strip()
                                       and len(request.POST.get(f"{nearby}-name").strip()) <= 5
                                    else ""
                                )
                            ),
                        },
                        f"{nearby}_distance": {
                            "valid": (
                                False
                                if request.POST.get(f"{nearby}-name").strip()
                                   and not request.POST.get(f"{nearby}-distance").strip()
                                else (
                                    False
                                    if request.POST.get(f"{nearby}-distance").strip()
                                       and request.POST.get(f"{nearby}-distance").strip()[0] == "-"
                                       and request.POST.get(f"{nearby}-distance").strip()[
                                           1:
                                           ].isdigit()
                                    else (
                                        False
                                        if request.POST.get(f"{nearby}-distance").strip()
                                           and not request.POST.get(f"{nearby}-distance").strip()
                                        .replace(",", "")
                                        .isdigit()
                                        else True
                                    )
                                )
                            ),
                            "message": (
                                "If you have provided the name, you must also provide the distance to it."
                                if request.POST.get(f"{nearby}-name").strip()
                                   and not request.POST.get(f"{nearby}-distance").strip()
                                else (
                                    "The distance must be greater than or equal 0."
                                    if request.POST.get(f"{nearby}-distance").strip()
                                       and request.POST.get(f"{nearby}-distance").strip()[0] == "-"
                                       and request.POST.get(f"{nearby}-distance").strip()[
                                           1:
                                           ].isdigit()
                                    else (
                                        "The distance must consist of positive digits."
                                        if request.POST.get(f"{nearby}-distance").strip()
                                           and not request.POST.get(f"{nearby}-distance").strip()
                                        .replace(",", "")
                                        .isdigit()
                                        else ""
                                    )
                                )
                            ),
                        },
                    }
                )
                response.update(
                    {
                        f"{name}": folder,
                    }
                )

            elif len(request.POST.getlist(f"{nearby}-name")) > 1:
                for n, d in zip(
                        request.POST.getlist(f"{nearby}-name"),
                        request.POST.getlist(f"{nearby}-distance"),
                ):
                    folder.append(
                        {
                            f"{nearby}_name": {
                                "valid": (
                                    False
                                    if d.strip() and not n.strip()
                                    else False if n.strip() and len(n.strip()) < 5 else True
                                ),
                                "message": (
                                    "If you have provided a distance, you must also provide a name."
                                    if d.strip() and not n.strip()
                                    else (
                                        "The name must be at least 5 characters long."
                                        if n.strip() and len(n.strip()) < 5
                                        else ""
                                    )
                                ),
                            },
                            f"{nearby}_distance": {
                                "valid": (
                                    False
                                    if n.strip() and not d.strip()
                                    else (
                                        False
                                        if d.strip() and d.strip()[0] == "-" and d.strip()[1:].isdigit()
                                        else (
                                            False
                                            if d.strip() and not d.strip().replace(",", "").isdigit()
                                            else True
                                        )
                                    )
                                ),
                                "message": (
                                    "If you've provided the name, you must also provide the distance to it."
                                    if n.strip() and not d.strip()
                                    else (
                                        "The distance must be greater than or equal 0."
                                        if d.strip() and d.strip()[0] == "-" and d.strip()[1:].isdigit()
                                        else (
                                            "The distance must consist of positive digits."
                                            if d.strip() and not d.strip().replace(",", "").isdigit()
                                            else ""
                                        )
                                    )
                                ),
                            },
                        },
                    )
                response.update(
                    {
                        f"{name}": folder,
                    }
                )

        validation = []

        for key in response:
            if isinstance(response[key], dict):
                validation.append(response[key].get("valid"))

            else:
                if isinstance(response[key], list):
                    for obj in response[key]:
                        if "valid" in obj.keys():
                            validation.append(obj["valid"])

                        else:
                            for k in obj.keys():
                                for item in obj[k].items():
                                    if item[0] == "valid":
                                        validation.append(item[1])

        if len(set(validation)) == 1 and validation[0] is not False:
            filters = {
                "user": request.user,
                "title": title.title(),
                "slug": "-".join(unidecode(title).lower().split(" ")),
                "description": description,
                "year_of_built": int(year_of_built),
                "price": float(price),
                "number_of_bedrooms": int(number_of_bedrooms),
                "number_of_bathrooms": int(number_of_bathrooms),
                "square_meters": float(square_meters),
                "parking_space": int(parking_space),
                "postal_code": postal_code,
                "country": request.POST["country"],
                "country_code": request.session["country_code"],
                "listing_status_id": ListingStatus.objects.get(name=request.POST.get("status").capitalize()).id,
                "category_id": Category.objects.get(name=request.POST.get("category").capitalize()).id,
            }

            geolocations_api = requests.get(
                url=f"https://api.geoapify.com/v1/geocode/search?text={request.POST['city']}&lang=en&limit=10&type=city&apiKey=52f8adced4b040d6a58ec4b7015ea9c1").json()[
                "features"]

            if request.POST.get("province"):
                filters["province"] = request.POST["province"]

                if request.POST.get("city"):
                    if City.objects.filter(name=request.POST.get("city")).exists():
                        city_id = City.objects.get(name=request.POST.get("city")).id
                        filters["city_id"] = city_id

                    else:
                        city = City(
                            name=request.POST.get("city"),
                            slug="-".join(request.POST.get("city").lower().split(" "))
                        )
                        filters["city"] = city
                        city.save()

                        for feature in geolocations_api:
                            if feature["properties"]["city"] == request.POST.get("city"):
                                filters["longitude"] = feature["properties"]["lon"]
                                filters["latitude"] = feature["properties"]["lat"]

                else:
                    if City.objects.filter(name=request.POST.get("province")).exists():
                        city_id = City.objects.get(name=request.POST.get("province")).id

                        filters["city_id"] = city_id

                    else:
                        city = City(name=request.POST.get("province"),
                                    slug="-".join(request.POST.get("province").lower().split(" ")))
                        filters["city"] = city
                        city.save()

            else:
                filters["province"] = request.POST.get("country")

                if request.POST.get("city"):
                    if City.objects.filter(name=request.POST.get("city")).exists():
                        city_id = City.objects.get(name=request.POST.get("city")).id
                        filters["city_id"] = city_id

                    else:
                        city = City(
                            name=request.POST.get("city"),
                            slug="-".join(request.POST.get("city").lower().split(" "))
                        )
                        filters["city"] = city
                        city.save()

                else:
                    if City.objects.filter(name=request.POST.get("country")).exists():
                        city_id = City.objects.get(name=request.POST.get("country")).id

                        filters["city_id"] = city_id

                    else:
                        city = City(name=request.POST.get("country"),
                                    slug="-".join(request.POST.get("country").lower().split(" ")))
                        filters["city"] = city
                        city.save()

            if request.FILES["thumbnail"]:
                thumbnail = request.FILES["thumbnail"]
                thumbnail.name = str(uuid.uuid4()) + "." + thumbnail.name.split(sep=".")[1]
                filters["thumbnail"] = thumbnail

            if request.FILES["video"]:
                video = request.FILES["video"]
                video.name = str(uuid.uuid4()) + "." + video.name.split(sep=".")[1]
                filters["video"] = video

            new_property = Property(**filters)
            new_property.save()

            if request.POST.get("amenities"):
                amenities = [
                    Amenities.objects.get(name=amenity) for amenity in request.POST.getlist("amenities")
                ]

                for amenity in amenities:
                    new_property.amenities.add(amenity)

            if request.FILES["gallery"]:
                gallery_images = [
                    setattr(image, 'name', str(uuid.uuid4()) + '.' + image.name.split('.')[-1]) or image
                    for image in request.FILES.getlist('gallery')]

                for image in gallery_images:
                    image = Img(image=image)
                    # image.save()
                    # new_property.images.add(image)

            # save education, health and medical, transportation, shopping
            if request.POST.get("education-name") or request.POST.get("health-name") or request.POST.get(
                    "transportation-name") or request.POST.get("shopping-name"):
                nearbies = ["education", "health", "transportation", "shopping"]
                temporary_folders = [[], [], [], []]
                classes = [Education, HealthAndMedical, Transportation, Shopping]
                fields = [new_property.education, new_property.health_and_medical, new_property.transportation,
                          new_property.shopping]

                for nearby, folder, cls, field in zip(nearbies, temporary_folders, classes, fields):
                    if len(request.POST.getlist(f"{nearby}-name")) == 1 and len(
                            request.POST.get(f"{nearby}-name")) != 0:
                        obj = cls(
                            name=request.POST[f"{nearby}-name"],
                            distance=int(request.POST[f"{nearby}-distance"]),
                            rate=randint(a=1, b=5),
                        )
                        # obj.save()
                        #
                        # field.add(obj)

                    else:
                        for n, d in zip(request.POST.getlist(f"{nearby}-name"),
                                        request.POST.getlist(f"{nearby}-distance")):
                            if len(n) > 0:
                                if not (n, d) in folder:
                                    folder.append((n, d))

                        for item in folder:
                            obj = cls(name=item[0], distance=int(item[1]), rate=randint(a=1, b=5))
                            # obj.save()
                            #
                            # field.add(obj)

            request.session["new_property"] = {
                "title": title.title(),
                "url": new_property.get_absolute_url(),
            }

            return JsonResponse(data={
                "url": 'properties',
            })

        return JsonResponse(data=response)


def add_to_favourites(request) -> django.http.response.JsonResponse:
    """
    The function handles the form for adding a property to favorites.
    If the property was already added to favorites by the user, the liking is removed.
    However, if the user adds the property to favorites for the first time, the liking is saved.
    The function utilizes the PATCH method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the data is updated in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == "PATCH":
        property_id = int(json.loads(s=request.body.decode("utf-8"))["propertyId"])
        property_obj = Property.objects.get(id=property_id)

        if request.user in property_obj.favourites.all():
            property_obj.favourites.remove(request.user)

            return JsonResponse(
                data={
                    "valid": True,
                    "propertyId": property_id,
                }
            )

        elif request.user not in property_obj.favourites.all():
            property_obj.favourites.add(request.user)
            property_obj.save()

            return JsonResponse(
                data={
                    "valid": True,
                    "propertyId": property_id,
                }
            )

        else:
            return JsonResponse(
                data={
                    "valid": False,
                }
            )


def property_details(
        request, category_slug, property_slug
) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the property-details template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        category_slug: str
        property_slug: str

    Returns
    ----------
        django.http.response.HttpResponse
    """
    category = Category.objects.get(slug=category_slug)
    property_obj = Property.objects.get(category=category, slug=property_slug)
    city = City.objects.get(name=property_obj.city)
    reviews = Review.objects.filter(property_id=property_obj.id)
    images = list(enumerate([img.image.url for img in property_obj.images.all()]))

    if property_obj.user.account_type == "Individual":
        profile = Individual.objects.get(user=property_obj.user)

    else:
        profile = Business.objects.get(user=property_obj.user)

    return render(
        request=request,
        template_name="properties/property-details.html",
        context={
            "title": property_obj.title,
            "property": property_obj,
            "profile": profile,
            "city": city,
            "images": images,
            "range": range(5),
            "reviews": reviews,
            "current_date": (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
        },
    )


def add_review(
        request, category_slug, property_slug
) -> django.http.response.JsonResponse:
    """
    The function handles a form for adding reviews to properties.
    It utilizes the POST method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Users can submit a textual review and a rating from 1 to 5 for the property.
    Only registered and logged-in users are allowed to fill out the form.
    After successful form validation, the review is saved to the database and awaits approval from the administrator.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        category_slug: str
        property_slug: str

    Returns
    ----------
        django.http.response.JsonResponse
    """
    category = Category.objects.get(slug=category_slug)
    property_obj = get_object_or_404(
        klass=Property, slug=property_slug, category=category
    )

    if request.method == "POST":
        data = json.loads(s=request.body.decode("utf-8"))

        rate = int([data[key] for key in data.keys()][0][0])
        content = [data[key] for key in data.keys()][1][0]
        content_field = [data[key] for key in data.keys()][1][1]
        content_label = [data[key] for key in data.keys()][1][2]
        spam_verification = [data[key] for key in data][-1]

        if len(spam_verification) != 0:
            return JsonResponse(
                data={
                    "valid": None,
                }
            )

        response = {
            "valid": False if len(content) == 0 else True,
            "field": content_field,
            "message": (
                f"The {content_label} field cannot be empty." if not content else ""
            ),
        }

        if response["valid"]:
            user = User.objects.get(username=request.user)
            review = Review(
                user=user, property=property_obj, rate=rate, content=content
            )
            review.save()

            return JsonResponse(
                data={
                    "valid": True,
                    "message": "The review has been submitted for approval by the administrator.",
                }
            )

        else:
            return JsonResponse(data=data, safe=False)


def schedule_tour(
        request, category_slug, property_slug
) -> django.http.response.JsonResponse:
    """
    The function handles a form for scheduling a visit with a property seller or landlord.
    It utilizes the POST method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Both logged-in and non-logged-in users have the option to schedule a visit.
    After successful form validation, an email message is sent to the seller requesting a meeting,
    and the meeting details are saved to the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        category_slug: str
        property_slug: str

    Returns
    ----------
        django.http.response.JsonResponse
    """
    category = Category.objects.get(slug=category_slug)
    property_obj = get_object_or_404(
        klass=Property, slug=property_slug, category=category
    )
    property_user_email = property_obj.user.email

    if request.method == "POST":
        data = json.loads(s=request.body.decode("utf-8"))
        date, time, name, phone_number, message = [
            i[0] for i in [data[key] for key in data][:-1]
        ]
        date_field, time_field, name_field, phone_number_field, message_field = [
            i[1] for i in [data[key] for key in data][:-1]
        ]
        date_label, time_label, name_label, phone_number_label, message_label = [
            i[2] for i in [data[key] for key in data][:-1]
        ]
        spam_verification = [data[key] for key in data][-1]

        if len(spam_verification) != 0:
            return JsonResponse(data={"valid": None})

        response = [
            {
                "valid": False if not date else True,
                "field": date_field,
                "message": (
                    f"You need to choose a meeting {date_label}." if not date else ""
                ),
            },
            {
                "valid": False if not time else True,
                "field": time_field,
                "message": (
                    f"You need to choose a meeting {time_label}." if not time else ""
                ),
            },
            {
                "valid": True,
                "field": name_field,
                "message": "",
            },
            {
                "valid": (
                    False
                    if not phone_number
                    else (
                        False
                        if not re.match(
                            pattern="^\\+?[1-9][0-9]{7,14}$", string=phone_number
                        )
                        else True
                    )
                ),
                "field": phone_number_field,
                "message": (
                    f"The {phone_number_label} cannot be empty."
                    if not phone_number
                    else (
                        f"Invalid {phone_number_label} number format."
                        if not re.match(
                            pattern="^\\+?[1-9][0-9]{7,14}$", string=phone_number
                        )
                        else ""
                    )
                ),
            },
            {
                "valid": True,
                "field": message_field,
                "message": "",
            },
        ]

        validation = [data["valid"] for data in response]

        if all(validation):
            if request.user.is_anonymous:
                user = User()
                user.save()

                tour_schedule = TourSchedule(
                    property=property_obj,
                    name=name,
                    date=date,
                    time=time,
                    phone_number=phone_number,
                    message=message,
                )
                tour_schedule.save()

                user.delete()
            else:
                tour_schedule = TourSchedule(
                    customer=request.user,
                    property=property_obj,
                    name=name,
                    date=date,
                    time=time,
                    phone_number=phone_number,
                    message=message,
                )
                tour_schedule.save()

            try:

                html_message = render_to_string(
                    template_name="properties/schedule_mail.html",
                    context={
                        "date": date,
                        "time": time,
                        "name": name,
                        "phone_number": phone_number,
                        "message": message,
                    },
                )

                plain_message = strip_tags(html_message)

                message = EmailMultiAlternatives(
                    subject="Meeting request from Global Estate Hub.",
                    body=plain_message,
                    from_email=os.environ.get("EMAIL_HOST_USER"),
                    to=[property_user_email],
                )

                message.attach_alternative(content=html_message, mimetype="text/html")
                message.send()

                return JsonResponse(
                    data={
                        "valid": True,
                        "message": "Your inquiry has been sent to the seller.",
                    }
                )

            except Exception:
                return JsonResponse(
                    data={
                        "valid": False,
                        "message": "The message could not be sent to the seller. Please try again.",
                    }
                )

        else:
            return JsonResponse(data=response, safe=False)
