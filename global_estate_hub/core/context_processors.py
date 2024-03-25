import os

from django.middleware.csrf import get_token
from properties.models import Property, Category, City
from django.db.models import Count


def generate_token(request) -> dict:
    """
    Generating CSRF middleware tokens for all forms in the project.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    return {
        'csrf_token': get_token(request=request)
    }


def properties_types(request) -> dict:
    """
    Returns all available property categories along with information such as category name,
    image source, URL address, and the number of properties in each category.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    return {
        'get_category_properties_info': list(
            zip(
                [category.name for category in Category.objects.all().order_by('-name')],
                [category.image.url for category in Category.objects.all().order_by('-name')],
                [category.get_absolute_url() for category in Category.objects.all().order_by('-name')],
                [Property.objects.filter(category=category).count() for category in
                 Category.objects.all().order_by('-name')]
            )
        ),
    }


def explore_cities(request) -> dict:
    """
    Returns all available property cities along with information such as city name,
    image source, URL address, and the number of properties in each city.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    return {
        'get_cities_info': list(
            zip(
                [city.name for city in City.objects.all().order_by('-name')],
                [city.image.url for city in City.objects.all().order_by('-name')],
                [city.get_absolute_url() for city in City.objects.all().order_by('-name')],
                [Property.objects.filter(city=city).count() for city in
                 City.objects.all().order_by('-name')]
            )
        ),
    }


def discover_cities(request) -> dict:
    """
    Returns the most frequently occurring cities in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    return {
        'discover_cities': [City.objects.get(name=obj.city.name) for obj in
                            Property.objects.annotate(city_count=Count('city'))][:8],
    }
