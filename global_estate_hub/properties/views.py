from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from .models import Property, ListingStatus, Category, City
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from unidecode import unidecode


def property_pagination(request, object_list, per_page):
    paginator = Paginator(object_list=object_list, per_page=per_page)
    page = request.GET.get('page')
    pages = paginator.get_page(number=page)

    if page is None:
        pages = paginator.get_page(number=1)

    else:
        if page not in list(str(i) for i in pages.paginator.page_range):
            return redirect(to='error')

    return pages


def properties_context():
    return {
        'listing_statuses': [obj.name for obj in ListingStatus.objects.all()],
        'categories': sorted(set([obj.category.name for obj in
                                  Property.objects.filter(listing_status=ListingStatus.objects.get(name='Rent'))])),
        'min_price': min(list(
            set([obj.price for obj in
                 Property.objects.filter(listing_status=ListingStatus.objects.get(name='Rent'))]))),
        'max_price': max(list(
            set([obj.price for obj in
                 Property.objects.filter(listing_status=ListingStatus.objects.get(name='Rent'))]))),
        'number_of_bedrooms': sorted(set([obj.number_of_bedrooms for obj in
                                          Property.objects.filter(
                                              listing_status=ListingStatus.objects.get(name='Rent'))])),
        'number_of_bathrooms': sorted(set([obj.number_of_bathrooms for obj in
                                           Property.objects.filter(
                                               listing_status=ListingStatus.objects.get(name='Rent'))])),
        'cities': sorted(set([obj.city.name for obj in
                              Property.objects.filter(listing_status=ListingStatus.objects.get(name='Rent'))])),
        'square_meters': sorted(set([obj.square_meters for obj in
                                     Property.objects.filter(listing_status=ListingStatus.objects.get(name='Rent'))])),
    }


def sidebar_context(listing_status=None, category=None, min_price=None, max_price=None, min_bedrooms=None,
                    max_bedrooms=None, min_bathrooms=None, max_bathrooms=None, location=None, min_square=None,
                    max_square=None):
    return {
        'listing_statuses': sorted(set([obj.name for obj in ListingStatus.objects.all()])),
        'categories':
            sorted(set([obj.category.name for obj in
                        Property.objects.filter(
                            listing_status_id=ListingStatus.objects.get(
                                slug='-'.join(listing_status.lower().split())).id
                        )])),
        'min_price':
            min(set([obj.price for obj in
                     Property.objects.filter(
                         listing_status_id=ListingStatus.objects.get(
                             slug='-'.join(listing_status.lower().split())).id
                     )])),
        'max_price':
            max(set([obj.price for obj in
                     Property.objects.filter(
                         listing_status_id=ListingStatus.objects.get(
                             slug='-'.join(listing_status.lower().split())).id
                     )])),
        'number_of_bedrooms':
            sorted(set([str(obj.number_of_bedrooms) for obj in Property.objects.filter(
                listing_status_id=ListingStatus.objects.get(
                    slug='-'.join(listing_status.lower().split())).id
            )])),
        'number_of_bathrooms':
            sorted(set([str(obj.number_of_bathrooms) for obj in Property.objects.filter(
                listing_status_id=ListingStatus.objects.get(
                    slug='-'.join(listing_status.lower().split())).id
            )])),
        'cities':
            sorted(set([obj.city.name for obj in
                        Property.objects.filter(listing_status_id=ListingStatus.objects.get(
                            slug='-'.join(listing_status.lower().split())).id
                                                )])),
        'square_meters':
            sorted(set([str(obj.square_meters) for obj in Property.objects.filter(
                listing_status_id=ListingStatus.objects.get(
                    slug='-'.join(listing_status.lower().split())).id
            )]))
    }


def properties_sorting():
    pass


def properties(request):
    queryset = []
    context = {}

    if request.GET:
        print('Request GET.')

        if 'properties-order' in request.GET:
            print('If properties order in request GET.')
            context.update(properties_context())
            if 'keyword' in request.session:
                print('Keyword in request session.')
                if 'Newest Properties' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = 'Newest Properties'
                    queryset.extend(Property.objects.filter(title__icontains=request.session.get('keyword')).order_by(
                        '-date_posted'))

                if 'Oldest Properties' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = 'Oldest Properties'
                    queryset.extend(Property.objects.filter(title__icontains=request.session.get('keyword')).order_by(
                        'date_posted'))

                if 'Alphabetically Ascending' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = 'Alphabetically Ascending'
                    queryset.extend(
                        Property.objects.filter(title__icontains=request.session.get('keyword')).order_by('title'))

                if 'Alphabetically Descending' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = 'Alphabetically Descending'
                    queryset.extend(
                        Property.objects.filter(title__icontains=request.session.get('keyword')).order_by('-title'))

            else:
                if 'Newest Properties' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.all().order_by('-date_posted'))

                if 'Oldest Properties' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.all().order_by('date_posted'))

                if 'Alphabetically Ascending' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.all().order_by('title'))

                if 'Alphabetically Descending' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')
                    queryset.extend(Property.objects.all().order_by('-title'))

        elif 'keyword' in request.GET:
            print('Elif keyword in request GET.')
            context.update(properties_context())
            request.session['sorted_type'] = 'Newest Properties'
            request.session['keyword'] = request.GET.get('keyword')
            keyword = request.GET.get('keyword')
            queryset.clear()
            queryset.extend(
                Property.objects.filter(title__icontains=keyword).order_by('-date_posted'))

        else:
            print('No properties order, keyword in request GET.')
            context.update(sidebar_context(listing_status=request.GET.get('status')))
            queryset.clear()
            queryset.extend(Property.objects.filter(listing_status_id=
                                                    ListingStatus.objects.get(
                                                        slug='-'.join(request.GET.get('status').lower().split())).id))

    else:
        print('No request GET.')
        context.update(properties_context())

        if request.session.get('sorted_type'):
            request.session.pop('sorted_type')

        if request.session.get('keyword'):
            request.session.pop('keyword')

        if request.session.get('filters'):
            request.session.pop('filters')

        if request.session.get('category'):
            request.session.pop('category')

        request.session['sorted_type'] = 'Newest Properties'
        queryset.extend(Property.objects.all().order_by('-date_posted'))

    context.update({
        'title': 'Properties',
        'properties': queryset,
        'sorted_type': request.session['sorted_type'],
        'pages': property_pagination(request=request, object_list=queryset, per_page=6),
    })
    return render(request=request, template_name='properties/properties.html', context=context)


def property_categories(request, category_slug):
    category = get_object_or_404(klass=Category, slug=category_slug)

    queryset = []

    if request.GET:
        if 'properties-order' in request.GET:
            if 'Newest Properties' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(category=category).order_by('-date_posted'))

            if 'Oldest Properties' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(category=category).order_by('date_posted'))

            if 'Alphabetically Ascending' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(category=category).order_by('title'))

            if 'Alphabetically Descending' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(category=category).order_by('-title'))

        else:
            if request.session.get('sorted_type'):
                request.session.pop('sorted_type')

            request.session['sorted_type'] = 'Newest Properties'
            queryset.extend(Property.objects.filter(category=category).order_by('-date_posted'))

    else:
        if request.session.get('sorted_type'):
            request.session.pop('sorted_type')

        if request.session.get('keyword'):
            request.session.pop('keyword')

        request.session['sorted_type'] = 'Newest Properties'
        queryset.extend(Property.objects.filter(category=category).order_by('-date_posted'))

    return render(request=request, template_name='properties/properties-category.html', context={
        'title': category,
        'category': category,
        'properties': queryset,
        'sorted_type': request.session['sorted_type'],
        'pages': property_pagination(request=request, object_list=queryset, per_page=6)
    })


def property_cities(request, city_slug):
    city = get_object_or_404(klass=City, slug=city_slug)

    queryset = []

    if request.GET:
        if 'properties-order' in request.GET:
            if 'Newest Properties' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(city=city).order_by('-date_posted'))

            if 'Oldest Properties' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(city=city).order_by('date_posted'))

            if 'Alphabetically Ascending' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(city=city).order_by('title'))

            if 'Alphabetically Descending' in request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(city=city).order_by('-title'))

        else:
            if request.session.get('sorted_type'):
                request.session.pop('sorted_type')

            request.session['sorted_type'] = 'Newest Properties'
            queryset.extend(Property.objects.filter(city=city).order_by('-date_posted'))

    else:
        if request.session.get('sorted_type'):
            request.session.pop('sorted_type')

        if request.session.get('keyword'):
            request.session.pop('keyword')

        request.session['sorted_type'] = 'Newest Properties'
        queryset.extend(Property.objects.filter(city=city).order_by('-date_posted'))

    return render(request=request, template_name='properties/properties-cities.html', context={
        'title': city,
        'city': city,
        'properties': queryset,
        'sorted_type': request.session['sorted_type'],
        'pages': property_pagination(request=request, object_list=queryset, per_page=6)
    })


@login_required(login_url='login')
def add_property(request):
    return render(request=request, template_name='properties/add-property.html', context={
        'title': 'Add Property',
    })


def add_to_favourites(request):
    """
    The function handles the form for adding a property to favorites.
    If the property was already added to favorites by the user, the liking is removed.
    However, if the user adds the property to favorites for the first time, the liking is saved.
    The function utilizes the PATCH method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the data is updated in the database.

    return: JsonResponse
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


def property_details(request, category_slug, property_slug):
    category = Category.objects.get(slug=category_slug)
    property_obj = Property.objects.get(category=category, slug=property_slug)

    return render(request=request, template_name='properties/property-details.html', context={
        'title': property_obj.title,
    })
