from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from .models import Property, ListingStatus, Category, City
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from itertools import chain


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


def properties(request):
    queryset = []

    if request.GET:
        if 'properties-order' in request.GET:
            if 'keyword' in request.session:
                if 'Newest Properties' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = 'Newest Properties'
                    queryset.extend(Property.objects.filter(title__icontains=request.session.get('keyword')).order_by(
                        '-date_posted'))

                elif 'Oldest Properties' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = 'Oldest Properties'
                    queryset.extend(Property.objects.filter(title__icontains=request.session.get('keyword')).order_by(
                        'date_posted'))

                elif 'Alphabetically Ascending' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = 'Alphabetically Ascending'
                    queryset.extend(
                        Property.objects.filter(title__icontains=request.session.get('keyword')).order_by('title'))

                elif 'Alphabetically Descending' in request.GET.get('properties-order'):
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
            request.session['sorted_type'] = 'Newest Properties'
            request.session['keyword'] = request.GET.get('keyword')
            keyword = request.GET.get('keyword')
            queryset.extend(
                Property.objects.filter(title__icontains=keyword).order_by('-date_posted'))

        else:
            if request.session.get('sorted_type'):
                request.session.pop('sorted_type')

            request.session['sorted_type'] = 'Newest Properties'
            queryset.extend(Property.objects.all().order_by('-date_posted'))

    else:
        if request.session.get('sorted_type'):
            request.session.pop('sorted_type')

        if request.session.get('keyword'):
            request.session.pop('keyword')

        request.session['sorted_type'] = 'Newest Properties'
        queryset.extend(Property.objects.all().order_by('-date_posted'))

    return render(request=request, template_name='properties/properties.html', context={
        'title': 'Properties',
        'properties': queryset,
        'sorted_type': request.session['sorted_type'],
        'pages': property_pagination(request=request, object_list=queryset, per_page=6),
        'listing_statuses': [obj.name for obj in ListingStatus.objects.all()],
        'categories': sorted([obj.name for obj in Category.objects.all()]),
        'min_price': min(list(set([obj.price for obj in Property.objects.all()]))),
        'max_price': max(list(set([obj.price for obj in Property.objects.all()]))),
        'number_of_bedrooms': sorted(set([obj.number_of_bedrooms for obj in Property.objects.all()])),
        'number_of_bathrooms': sorted(set([obj.number_of_bathrooms for obj in Property.objects.all()])),
        'cities': sorted(set([obj.name for obj in City.objects.all()])),
        'square_meters': sorted(set([obj.square_meters for obj in Property.objects.all()])),
    })


def update_filters(request):
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))
        # print(f'Received -> {data}')
        print('stara')

        chosen_categories = sorted(set([c.category.name for c in
                                        Property.objects.filter(
                                            listing_status=ListingStatus.objects.get(name='Rent'))])) if data.get(
            'chosenStatus') == 'rent' else sorted(set([c.name for c in Category.objects.all()]))

        # jeśli jest listing status i jest category
        # jeśli jest listing status i nie ma category
        # jeśli nie ma listing status a jest category
        # jeśli nie ma listing statusa i nie ma category

        response = {
            'categories': sorted(set([(obj.category.slug, obj.category.name) for obj in Property.objects.filter(
                listing_status=ListingStatus.objects.get(
                    name=data.get('chosenStatus').capitalize()))])) if data.get('chosenStatus') else sorted(
                set([(obj.category.slug, obj.category.name) for obj in Property.objects.all()])),
            'price_range': [
                min([obj.price for obj in list(chain(*[Property.objects.filter(listing_status=ListingStatus.objects.get(name=data.get('chosenStatus').capitalize()), category_id=Category.objects.get(name=c.capitalize())) for c in data.get('chosenCategories')]))]) if data.get('chosenStatus') and data.get('chosenCategories') else
                min([obj.price for obj in list(chain(*[Property.objects.filter(listing_status=ListingStatus.objects.get(name=data.get('chosenStatus').capitalize()), category_id=Category.objects.get(name=c.capitalize())) for c in chosen_categories]))]) if data.get('chosenStatus') and not data.get('chosenCategory') else
                min([obj.price for obj in list(chain(*[Property.objects.filter(category_id=Category.objects.get(name=c.capitalize())) for c in data.get('chosenCategories')]))]) if data.get('chosenCategories') and not data.get('chosenStatus') else
                min([obj.price for obj in list(chain(*[Property.objects.filter(category_id=Category.objects.get(name=c.capitalize())) for c in chosen_categories]))]),

                max([obj.price for obj in list(chain(*[Property.objects.filter(
                    listing_status=ListingStatus.objects.get(name=data.get('chosenStatus').capitalize()),
                    category_id=Category.objects.get(name=c.capitalize())) for c in
                    data.get('chosenCategories')]))]) if data.get(
                    'chosenStatus') and data.get('chosenCategories') else
                max([obj.price for obj in list(chain(*[Property.objects.filter(
                    listing_status=ListingStatus.objects.get(name=data.get('chosenStatus').capitalize()),
                    category_id=Category.objects.get(name=c.capitalize())) for c in chosen_categories]))]) if data.get(
                    'chosenStatus') and not data.get('chosenCategory') else
                max([obj.price for obj in list(chain(
                    *[Property.objects.filter(category_id=Category.objects.get(name=c.capitalize())) for c in
                      data.get('chosenCategories')]))]) if data.get('chosenCategories') and not data.get(
                    'chosenStatus') else
                max([obj.price for obj in list(chain(
                    *[Property.objects.filter(category_id=Category.objects.get(name=c.capitalize())) for c in
                      chosen_categories]))]),
            ],
            'min_bedrooms': [],
            'max_bedrooms': [],
            'min_bathrooms': [],
            'max_bathrooms': [],
            'location': [],
            'min_meters': [],
            'max_meters': [],
        }
        print(f'Sent -> {response}')

        return JsonResponse(data=response)


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


def property_details(request, property_slug):
    property_obj = Property.objects.get(slug=property_slug)

    return render(request=request, template_name='properties/property-details.html', context={
        'title': property_obj.title,
    })
