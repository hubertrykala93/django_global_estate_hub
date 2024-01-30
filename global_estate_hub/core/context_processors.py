from django.middleware.csrf import get_token
from properties.models import Property, Category, City
from itertools import chain


def breadcrumbs_urls(request) -> dict:
    """
    Creating breadcrumbs for the entire project.

    return: dict
    """
    arr = request.path.split(sep='/')[1:]
    titles = [title.replace('-', ' ').title() for title in arr]
    paths = []

    for parent_index, parent_loop in enumerate(arr):
        path = ''

        for child_index, child_loop in enumerate(arr):
            if child_index <= parent_index:
                path += '/' + child_loop

        paths.append(path)

    titles = titles[:-1]
    paths = paths[:-1]

    return {
        'urls': list(zip(titles, paths))
    }


def generate_token(request) -> dict:
    """
    Generating CSRF middleware tokens for all forms in the project.

    return: dict
    """
    return {
        'csrf_token': get_token(request=request)
    }


def properties_types(request):
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


def explore_cities(request):
    print(list(
            zip(
                [city.name for city in City.objects.all().order_by('-name')],
                [city.image.url for city in City.objects.all().order_by('-name')],
                [city.get_absolute_url() for city in City.objects.all().order_by('-name')],
                [Property.objects.filter(city=city).count() for city in
                 City.objects.all().order_by('-name')]
            )))
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


def discover_cities(request):
    return {
        'discover_cities': [p.city for p in
                            list(chain(*[Property.objects.filter(city=c) for c in City.objects.all()]))][:8],
    }
