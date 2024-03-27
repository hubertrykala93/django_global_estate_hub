import django.core.paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
import re
import os
from accounts.models import User, Individual, Business
from .models import Property, ListingStatus, Category, City, Review, TourSchedule
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from unidecode import unidecode
from datetime import datetime
from datetime import timedelta
from django.db.models import Min, Max


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
    page = request.GET.get('page')
    pages = paginator.get_page(number=page)

    if page is None:
        pages = paginator.get_page(number=1)

    else:
        if page not in list(str(i) for i in pages.paginator.page_range):
            return redirect(to='error')

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
        'listing_statuses': ListingStatus.objects.all().order_by('name'),
        'categories': Property.objects.filter(listing_status_id=ListingStatus.objects.get(name='Rent').id).values_list(
            'category__name', flat=True).order_by('category__name').distinct(),
        'number_of_bedrooms': [str(obj) for obj in
                               Property.objects.filter(
                                   listing_status_id=ListingStatus.objects.get(name='Rent').id).values_list(
                                   'number_of_bedrooms', flat=True).order_by('number_of_bedrooms').distinct()],
        'number_of_bathrooms': [str(obj) for obj in
                                Property.objects.filter(
                                    listing_status_id=ListingStatus.objects.get(name='Rent').id).values_list(
                                    'number_of_bathrooms', flat=True).order_by('number_of_bathrooms').distinct()],
        'cities': Property.objects.filter(listing_status_id=ListingStatus.objects.get(name='Rent').id).values_list(
            'city__name', flat=True).order_by('city__name').distinct(),
        'square_meters': [str(obj) for obj in
                          Property.objects.filter(
                              listing_status_id=ListingStatus.objects.get(name='Rent').id).values_list(
                              'square_meters', flat=True).order_by('square_meters').distinct()],
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
        'listing_statuses': ListingStatus.objects.all().order_by('name'),
        'categories': Property.objects.filter(listing_status_id=kwargs['listing_status_id']).values_list(
            'category__name', flat=True).order_by('category__name').distinct(),
        'number_of_bedrooms': [str(obj) for obj in
                               Property.objects.filter(**kwargs).values_list('number_of_bedrooms', flat=True).order_by(
                                   'number_of_bedrooms').distinct()],
        'number_of_bathrooms': [str(obj) for obj in Property.objects.filter(**kwargs).values_list('number_of_bathrooms',
                                                                                                  flat=True).order_by(
            'number_of_bathrooms').distinct()],
        'cities': Property.objects.filter(listing_status_id=kwargs['listing_status_id']).values_list('city__name',
                                                                                                     flat=True).order_by(
            'city__name').distinct(),
        'square_meters': [str(obj) for obj in
                          Property.objects.filter(**kwargs).values_list('square_meters', flat=True).order_by(
                              'square_meters').distinct()],
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
        if 'properties-order' in request.GET:
            if 'keyword' in request.session:
                if request.session.get('filters'):
                    request.session.pop('filters')

                if request.session.get('checked_filters'):
                    request.session.pop('checked_filters')

                context.update(properties_context())

                if 'Newest Properties' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.filter(title__icontains=request.session['keyword']).order_by(
                        '-date_posted'))

                elif 'Oldest Properties' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.filter(title__icontains=request.session['keyword']).order_by(
                        'date_posted'))

                elif 'Price Ascending' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(
                        Property.objects.filter(title__icontains=request.session['keyword']).order_by('price'))

                elif 'Price Descending' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(
                        Property.objects.filter(title__icontains=request.session['keyword']).order_by('-price'))

                elif 'Featured' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(
                        Property.objects.filter(title__icontains=request.session['keyword']).order_by(
                            '-is_featured'))

                else:
                    request.session['sorted_type'] = 'Newest Properties'
                    queryset.extend(Property.objects.filter(title__icontains=request.session['keyword']).order_by(
                        '-date_posted'))

            elif 'filters' in request.session:
                context.update(sidebar_context(**request.session['filters']))

                if 'Newest Properties' in request.GET.get('properties-order'):
                    if request.session.get('filters').get('is_featured'):
                        request.session.get('filters').pop('is_featured')

                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.filter(**request.session['filters']).order_by('-date_posted'))

                elif 'Oldest Properties' in request.GET.get('properties-order'):
                    if request.session.get('filters').get('is_featured'):
                        request.session.get('filters').pop('is_featured')

                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.filter(**request.session['filters']).order_by('date_posted'))

                elif 'Price Ascending' in request.GET.get('properties-order'):
                    if request.session.get('filters').get('is_featured'):
                        request.session.get('filters').pop('is_featured')

                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.filter(**request.session['filters']).order_by('price'))

                elif 'Price Descending' in request.GET.get('properties-order'):
                    if request.session.get('filters').get('is_featured'):
                        request.session.get('filters').pop('is_featured')

                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.filter(**request.session['filters']).order_by('-price'))

                elif 'Featured' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.filter(**request.session['filters']).order_by('-is_featured'))

                else:
                    if request.session.get('filters').get('is_featured'):
                        request.session.get('filters').pop('is_featured')

                    request.session['sorted_type'] = 'Newest Properties'
                    queryset.extend(Property.objects.filter(**request.session['filters']).order_by('-date_posted'))

            else:
                context.update(properties_context())

                if 'Newest Properties' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.all().order_by('-date_posted'))

                elif 'Oldest Properties' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.all().order_by('date_posted'))

                elif 'Price Ascending' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.all().order_by('price'))

                elif 'Price Descending' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.all().order_by('-price'))

                elif 'Featured' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.all().order_by('-is_featured'))

                else:
                    request.session['sorted_type'] = 'Newest Properties'
                    queryset.extend(Property.objects.all().order_by('-date_posted'))

        elif 'keyword' in request.GET:
            if request.session.get('checked_filters'):
                request.session.pop('checked_filters')

            context.update(properties_context())

            request.session['sorted_type'] = 'Newest Properties'
            request.session['keyword'] = request.GET.get('keyword')
            queryset.extend(
                Property.objects.filter(title__icontains=request.GET.get('keyword')).order_by('-date_posted'))

        elif 'status' in request.GET or 'category' in request.GET or 'min_price' in request.GET or \
                'max_price' in request.GET or 'min_bedrooms' in request.GET or 'max_bedrooms' in request.GET or \
                'min_bathrooms' in request.GET or 'max_bathrooms' in request.GET or 'location' in request.GET or \
                'min_square' in request.GET or 'max_square' in request.GET:

            if request.session.get('keyword'):
                request.session.pop('keyword')

            if 'status' in request.GET:
                filters['listing_status_id'] = ListingStatus.objects.get(
                    slug='-'.join(request.GET.get('status').lower().split())).id

                if len(Property.objects.filter(**filters)) == 0:
                    queryset.clear()

                request.session['sorted_type'] = 'Newest Properties'
                request.session['filters'] = filters
                checked_filters.update(
                    {
                        'checked_status': request.GET.get('status').capitalize(),
                    }
                )
                request.session['checked_filters'] = checked_filters

                context.update(sidebar_context(**filters))
                queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

            if 'category' in request.GET:
                filters['category__pk__in'] = [Category.objects.get(slug='-'.join(obj.lower().split())).id for
                                               obj in request.GET.getlist('category')]

                if len(Property.objects.filter(**filters)) == 0:
                    queryset.clear()

                else:
                    checked_categories = request.GET.getlist('category')
                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_categories': [category.capitalize() for category in
                                                   request.GET.getlist('category')],
                        }
                    )
                    request.session['checked_filters'] = checked_filters

                    context.update({
                        'checked_categories': checked_categories,
                    })
                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

            if 'min_bedrooms' in request.GET:
                if 'max_bedrooms' in request.GET:
                    filters['number_of_bedrooms__range'] = [int(request.GET.get('min_bedrooms')),
                                                            int(request.GET.get('max_bedrooms'))]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_min_bedrooms': request.GET.get('min_bedrooms'),
                            'checked_max_bedrooms': request.GET.get('max_bedrooms'),
                        }
                    )
                    request.session['checked_filters'] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

                else:
                    filters['number_of_bedrooms__range'] = [
                        int(request.GET.get('min_bedrooms')),
                        Property.objects.aggregate(Max('number_of_bedrooms'))['number_of_bedrooms__max']
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_min_bedrooms': request.GET.get('min_bedrooms'),
                        }
                    )
                    request.session['checked_filters'] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

            if 'max_bedrooms' in request.GET:

                if 'min_bedrooms' in request.GET:
                    filters['number_of_bedrooms__range'] = [int(request.GET.get('min_bedrooms')),
                                                            int(request.GET.get('max_bedrooms'))]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_min_bedrooms': request.GET.get('min_bedrooms'),
                            'checked_max_bedrooms': request.GET.get('max_bedrooms'),
                        }
                    )
                    request.session['checked_filters'] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

                else:
                    filters['number_of_bedrooms__range'] = [
                        Property.objects.aggregate(Min('number_of_bedrooms'))['number_of_bedrooms__min'],
                        int(request.GET.get('max_bedrooms'))
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_max_bedrooms': request.GET.get('max_bedrooms'),
                        }
                    )

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

            if 'min_bathrooms' in request.GET:
                if 'max_bathrooms' in request.GET:
                    filters['number_of_bathrooms__range'] = [int(request.GET.get('min_bathrooms')),
                                                             int(request.GET.get('max_bathrooms'))]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_min_bathrooms': request.GET.get('min_bathrooms'),
                            'checked_max_bathrooms': request.GET.get('max_bathrooms'),
                        }
                    )
                    request.session['checked_filters'] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

                else:
                    filters['number_of_bathrooms__range'] = [
                        int(request.GET.get('min_bathrooms')),
                        Property.objects.aggregate(Max('number_of_bathrooms'))['number_of_bathrooms__max']
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_min_bathrooms': request.GET.get('min_bathrooms'),
                        }
                    )
                    request.session['checked_filters'] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

            if 'max_bathrooms' in request.GET:
                if 'min_bathrooms' in request.GET:
                    filters['number_of_bathrooms__range'] = [int(request.GET.get('min_bathrooms')),
                                                             int(request.GET.get('max_bathrooms'))]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_min_bathrooms': request.GET.get('min_bathrooms'),
                            'checked_max_bathrooms': request.GET.get('max_bathrooms'),
                        }
                    )
                    request.session['checked_filters'] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

                else:
                    filters['number_of_bathrooms__range'] = [
                        Property.objects.aggregate(Min('number_of_bathrooms'))['number_of_bathrooms__min'],
                        int(request.GET.get('max_bathrooms'))
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_max_bathrooms': request.GET.get('max_bathrooms'),
                        }
                    )
                    request.session['checked_filters'] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

            if 'location' in request.GET:
                filters['city__id'] = City.objects.get(
                    slug=unidecode('-'.join(request.GET.get('location').lower().split()))).id

                if len(Property.objects.filter(**filters)) == 0:
                    queryset.clear()

                request.session['sorted_type'] = 'Newest Properties'
                request.session['filters'] = filters
                checked_filters.update(
                    {
                        'city': request.GET.get('location').capitalize(),
                    }
                )
                request.session['checked_filters'] = checked_filters

                context.update(sidebar_context(**filters))

                queryset.clear()
                queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

            if 'min_square' in request.GET:
                if 'max_square' in request.GET:
                    filters['square_meters__range'] = [float(request.GET.get('min_square')),
                                                       float(request.GET.get('max_square'))]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_min_square': request.GET.get('min_square'),
                            'checked_max_square': request.GET.get('max_square'),
                        }
                    )
                    request.session['checked_filters'] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

                else:
                    filters['square_meters__range'] = [
                        float(request.GET.get('min_square')),
                        Property.objects.aggregate(Max('square_meters'))['square_meters__max']
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_min_square': request.GET.get('min_square'),
                        }
                    )
                    request.session['checked_filters'] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

            if 'max_square' in request.GET:
                if 'min_square' in request.GET:
                    filters['square_meters__range'] = [float(request.GET.get('min_square')),
                                                       float(request.GET.get('max_square'))]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_min_square': request.GET.get('min_square'),
                            'checked_max_square': request.GET.get('max_square'),
                        }
                    )
                    request.session['checked_filters'] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

                else:
                    filters['square_meters__range'] = [
                        Property.objects.aggregate(Min('square_meters'))['square_meters__min'],
                        float(request.GET.get('max_square'))
                    ]

                    if len(Property.objects.filter(**filters)) == 0:
                        queryset.clear()

                    request.session['sorted_type'] = 'Newest Properties'
                    request.session['filters'] = filters
                    checked_filters.update(
                        {
                            'checked_max_square': request.GET.get('max_square'),
                        }
                    )
                    request.session['checked_filters'] = checked_filters

                    context.update(sidebar_context(**filters))

                    queryset.clear()
                    queryset.extend(Property.objects.filter(**filters).order_by('-date_posted'))

        else:
            context.update(properties_context())

            if request.session.get('sorted_type'):
                request.session.pop('sorted_type')

            request.session['sorted_type'] = 'Newest Properties'
            queryset.extend(Property.objects.all().order_by('-date_posted'))

    else:
        if request.session.get('sorted_type'):
            request.session.pop('sorted_type')

        if request.session.get('keyword'):
            request.session.pop('keyword')

        if request.session.get('filters'):
            request.session.pop('filters')

        if request.session.get('checked_filters'):
            request.session.pop('checked_filters')

        request.session['sorted_type'] = 'Newest Properties'
        queryset.extend(Property.objects.all().order_by('-date_posted'))

        context.update(properties_context())

    context.update({
        'title': 'Properties',
        'properties': len(queryset),
        'sorted_type': request.session['sorted_type'],
        'pages': property_pagination(request=request, object_list=queryset, per_page=6),
    })

    return render(request=request, template_name='properties/properties.html', context=context)


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
        if 'properties-order' in request.GET:
            if 'Newest Properties' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(category=category).order_by('-date_posted'))

            elif 'Oldest Properties' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(category=category).order_by('date_posted'))

            elif 'Price Ascending' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(category=category).order_by('price'))

            elif 'Price Descending' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(category=category).order_by('-price'))

            elif 'Featured' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(category=category).order_by('-is_featured'))

            else:
                request.session['sorted_type'] = 'Newest Properties'
                queryset.extend(Property.objects.filter(category=category).order_by('-date_posted'))

        else:
            if request.session.get('sorted_type'):
                request.session.pop('sorted_type')

            request.session['sorted_type'] = 'Newest Properties'
            queryset.extend(Property.objects.filter(category=category).order_by('-date_posted'))

    else:
        if request.session.get('sorted_type'):
            request.session.pop('sorted_type')

        request.session['sorted_type'] = 'Newest Properties'
        queryset.extend(Property.objects.filter(category=category).order_by('-date_posted'))

    return render(request=request, template_name='properties/properties-category.html', context={
        'title': f'{category} Properties',
        'category': category,
        'properties': queryset,
        'sorted_type': request.session['sorted_type'],
        'pages': property_pagination(request=request, object_list=queryset, per_page=6)
    })


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
        if 'properties-order' in request.GET:
            if 'Newest Properties' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(city=city).order_by('-date_posted'))

            elif 'Oldest Properties' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(city=city).order_by('date_posted'))

            elif 'Price Ascending' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(city=city).order_by('price'))

            elif 'Price Descending' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(city=city).order_by('-price'))

            elif 'Featured' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(city=city).order_by('-is_featured'))

            else:
                request.session['sorted_type'] = 'Newest Properties'
                queryset.extend(Property.objects.filter(city=city).order_by('-date_posted'))

        else:
            if request.session.get('sorted_type'):
                request.session.pop('sorted_type')

            request.session['sorted_type'] = 'Newest Properties'
            queryset.extend(Property.objects.filter(city=city).order_by('-date_posted'))

    else:
        if request.session.get('sorted_type'):
            request.session.pop('sorted_type')

        request.session['sorted_type'] = 'Newest Properties'
        queryset.extend(Property.objects.filter(city=city).order_by('-date_posted'))

    return render(request=request, template_name='properties/properties-cities.html', context={
        'title': f'{city} Properties',
        'city': city,
        'properties': queryset,
        'sorted_type': request.session['sorted_type'],
        'pages': property_pagination(request=request, object_list=queryset, per_page=6)
    })


@login_required(login_url='login')
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
    return render(request=request, template_name='properties/add-property.html', context={
        'title': 'Add Property',
    })


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
    if request.method == 'PATCH':
        property_id = int(json.loads(s=request.body.decode('utf-8'))['propertyId'])
        property_obj = Property.objects.get(id=property_id)

        if request.user in property_obj.favourites.all():
            property_obj.favourites.remove(request.user)

            return JsonResponse(data={
                "valid": True,
                "propertyId": property_id,
            })

        elif request.user not in property_obj.favourites.all():
            property_obj.favourites.add(request.user)
            property_obj.save()

            return JsonResponse(data={
                "valid": True,
                "propertyId": property_id,
            })

        else:
            return JsonResponse(data={
                "valid": False,
            })


def property_details(request, category_slug, property_slug) -> django.http.response.HttpResponse:
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

    if property_obj.user.account_type == 'Individual':
        profile = Individual.objects.get(user=property_obj.user)

    else:
        profile = Business.objects.get(user=property_obj.user)

    properties = [p.user for p in Property.objects.all()]
    print(len(properties))

    return render(request=request, template_name='properties/property-details.html', context={
        'title': property_obj.title,
        'property': property_obj,
        'profile': profile,
        'city': city,
        'images': images,
        'range': range(5),
        'reviews': reviews,
        'current_date': (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
    })


def add_review(request, category_slug, property_slug) -> django.http.response.JsonResponse:
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
    property_obj = get_object_or_404(klass=Property, slug=property_slug, category=category)

    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        rate = int([data[key] for key in data.keys()][0][0])
        content = [data[key] for key in data.keys()][1][0]
        content_field = [data[key] for key in data.keys()][1][1]
        content_label = [data[key] for key in data.keys()][1][2]
        spam_verification = [data[key] for key in data][-1]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
            })

        response = {
            "valid":
                False if len(content) == 0 else
                True,
            "field": content_field,
            "message":
                f"The {content_label} field cannot be empty." if not content else
                ""
        }

        if response['valid']:
            user = User.objects.get(username=request.user)
            review = Review(user=user, property=property_obj, rate=rate, content=content)
            review.save()

            return JsonResponse(data={
                "valid": True,
                "message": "The review has been submitted for approval by the administrator.",
            })

        else:
            return JsonResponse(data=data, safe=False)


def schedule_tour(request, category_slug, property_slug) -> django.http.response.JsonResponse:
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
    property_obj = get_object_or_404(klass=Property, slug=property_slug, category=category)
    property_user_email = property_obj.user.email

    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))
        date, time, name, phone_number, message = [i[0] for i in [data[key] for key in data][:-1]]
        date_field, time_field, name_field, phone_number_field, message_field = [i[1] for i in
                                                                                 [data[key] for key in data][:-1]]
        date_label, time_label, name_label, phone_number_label, message_label = [i[2] for i in
                                                                                 [data[key] for key in data][:-1]]
        spam_verification = [data[key] for key in data][-1]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None
            })

        response = [
            {
                "valid":
                    False if not date else
                    True,
                "field": date_field,
                "message":
                    f"You need to choose a meeting {date_label}." if not date else
                    "",
            },
            {
                "valid":
                    False if not time else
                    True,
                "field": time_field,
                "message":
                    f"You need to choose a meeting {time_label}." if not time else
                    "",
            },
            {
                "valid": True,
                "field": name_field,
                "message": "",
            },
            {
                "valid":
                    False if not phone_number else
                    False if not re.match(pattern="^\\+?[1-9][0-9]{7,14}$", string=phone_number) else
                    True,
                "field": phone_number_field,
                "message":
                    f"The {phone_number_label} cannot be empty." if not phone_number else
                    f"Invalid {phone_number_label} number format." if not re.match(pattern="^\\+?[1-9][0-9]{7,14}$",
                                                                                   string=phone_number) else
                    "",
            },
            {
                "valid": True,
                "field": message_field,
                "message": "",
            }
        ]

        validation = [data['valid'] for data in response]

        if all(validation):
            if request.user.is_anonymous:
                user = User()
                user.save()

                tour_schedule = TourSchedule(property=property_obj, name=name,
                                             date=date, time=time, phone_number=phone_number, message=message)
                tour_schedule.save()

                user.delete()
            else:
                tour_schedule = TourSchedule(customer=request.user, property=property_obj, name=name,
                                             date=date, time=time, phone_number=phone_number, message=message)
                tour_schedule.save()

            try:

                html_message = render_to_string(
                    template_name='properties/schedule_mail.html',
                    context={
                        'date': date,
                        'time': time,
                        'name': name,
                        'phone_number': phone_number,
                        'message': message
                    }
                )

                plain_message = strip_tags(html_message)

                message = EmailMultiAlternatives(
                    subject='Meeting request from Global Estate Hub.',
                    body=plain_message,
                    from_email=os.environ.get("EMAIL_HOST_USER"),
                    to=[property_user_email]
                )

                message.attach_alternative(content=html_message, mimetype='text/html')
                message.send()

                return JsonResponse(data={
                    "valid": True,
                    "message": "Your inquiry has been sent to the seller.",
                })

            except Exception:
                return JsonResponse(data={
                    "valid": False,
                    "message": "The message could not be sent to the seller. Please try again.",
                })

        else:
            return JsonResponse(data=response, safe=False)
