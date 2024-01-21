from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import Property, ListingStatus, Category
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def property_context(obj: dict = None):
    rent_status_id = ListingStatus.objects.get(name='Rent').id

    context = {
        'listing_statuses': ListingStatus.objects.all(),
        'categories': sorted(
            list(set([obj.category.name for obj in Property.objects.filter(listing_status_id=rent_status_id)]))),
        'min_price': min([obj.price for obj in Property.objects.filter(listing_status_id=rent_status_id)]),
        'max_price': max([obj.price for obj in Property.objects.filter(listing_status_id=rent_status_id)]),
        'number_of_bedrooms': sorted(
            list(set([obj.number_of_bedrooms for obj in
                      Property.objects.filter(listing_status_id=rent_status_id)]))),
        'number_of_bathrooms': sorted(
            list(set([obj.number_of_bathrooms for obj in
                      Property.objects.filter(listing_status_id=rent_status_id)]))),
        'cities': sorted(
            list(set(obj.city.name for obj in Property.objects.filter(listing_status_id=rent_status_id)))),
        'square_meters': sorted(
            list(
                set([int(obj.square_meters) for obj in Property.objects.filter(listing_status_id=rent_status_id)])))
    }

    if obj is None:
        return context

    else:
        context.update(obj)

        return context


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
    rent_status_id = ListingStatus.objects.get(name='Rent').id

    if request.session.get('sorted_type'):
        request.session.pop('sorted_type')

    if request.session.get('keyword'):
        request.session.pop('keyword')

    if request.GET:
        print('Request GET.')

        if 'properties-order' in request.GET:
            print('Properties Order in request GET.')

            if 'Newest Properties' in request.GET.get('properties-order'):
                print('Newest Properties.')
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(listing_status=rent_status_id).order_by('-date_posted'))

            if 'Oldest Properties' in request.GET.get('properties-order'):
                print('Oldest Properties.')
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(listing_status=rent_status_id).order_by('date_posted'))

            if 'Alphabetically Ascending' in request.GET.get('properties-order'):
                print('Alphabetically Ascending.')
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(listing_status=rent_status_id).order_by('title'))

            if 'Alphabetically Descending' in request.GET.get('properties-order'):
                print(request.GET)
                print('Alphabetically Descending.')
                request.session['sorted_type'] = request.GET.get('properties-order')
                queryset.extend(Property.objects.filter(listing_status=rent_status_id).order_by('-title'))

        else:
            print('Properties Order not in request GET.')
            request.session['sorted_type'] = 'Newest Properties'
            queryset.extend(Property.objects.filter(listing_status=rent_status_id).order_by('-date_posted'))

    else:
        print('No request GET.')
        request.session['sorted_type'] = 'Newest Properties'
        queryset.extend(Property.objects.filter(listing_status=rent_status_id).order_by('-date_posted'))

    context = property_context(obj={
        'title': 'Properties',
        'properties': queryset,
        'sorted_type': request.session['sorted_type'],
        'pages': property_pagination(request=request, object_list=queryset, per_page=6),
    })

    return render(request=request, template_name='properties/properties.html', context=context)


def property_results(request):
    queryset = []
    rent_status_id = ListingStatus.objects.get(name='Rent').id

    if 'keyword' in request.GET:
        print('Keyword in request GET.')
        keyword = request.GET.get('keyword')
        request.session['keyword'] = request.GET.get('keyword')
        queryset.extend(
            Property.objects.filter(title__icontains=keyword, listing_status=rent_status_id).order_by('-date_posted'))

    elif 'properties-order' in request.GET:
        print('Elif properties-order in request GET.')
        if 'Newest Properties' in request.GET.get('properties-order'):
            print('Newest Properties in request GET get properties-order')
            request.session['sorted_type'] = 'Newest Properties'
            queryset.extend(Property.objects.filter(title__icontains=request.session.get('keyword'),
                                                    listing_status=rent_status_id).order_by('-date_posted'))

        elif 'Oldest Properties' in request.GET.get('properties-order'):
            print('Oldest Properties in request GET get properties-order.')
            request.session['sorted_type'] = 'Oldest Properties'
            queryset.extend(Property.objects.filter(title__icontains=request.session.get('keyword'),
                                                    listing_status=rent_status_id).order_by('date_posted'))

        elif 'Alphabetically Ascending' in request.GET.get('properties-order'):
            print('Alphabetically Ascending in request GET get properties-order.')
            request.session['sorted_type'] = 'Alphabetically Ascending'
            queryset.extend(
                Property.objects.filter(title__icontains=request.session.get('keyword'),
                                        listing_status=rent_status_id).order_by('title'))

        elif 'Alphabetically Descending' in request.GET.get('properties-order'):
            print('Alphabetically Descending in request GET get properties-order.')
            request.session['sorted_type'] = 'Alphabetically Descending'
            queryset.extend(Property.objects.filter(title__icontains=request.session.get('keyword'),
                                                    listing_status=rent_status_id).order_by('-title'))

    else:
        print('Else.')
        request.session['sorted_type'] = 'Newest Properties'
        queryset.extend(Property.objects.filter(title__icontains=request.session.get('keyword'),
                                                listing_status=rent_status_id).order_by('-date_posted'))

    context = property_context(obj={
        'title': 'Property Results',
        'properties': queryset,
        'sorted_type': request.session['sorted_type'],
        'pages': property_pagination(request=request, object_list=queryset, per_page=6),
    })

    return render(request=request, template_name='properties/property-results.html', context=context)


def update_filters(request):
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        response = {}

        # selected status name
        selected_status = data['chosenStatus']

        # selected status id
        selected_status_id = ListingStatus.objects.get(name=selected_status.capitalize()).id

        # queryset for selected status
        selected_status_queryset = Property.objects.filter(listing_status_id=selected_status_id)

        # minimum & maximum price of selected status queryset
        min_price_of_selected_queryset = min([obj.price for obj in selected_status_queryset])
        max_price_of_selected_queryset = max([obj.price for obj in selected_status_queryset])

        # selected categories names
        selected_categories = [name.capitalize() for name in data['chosenCategories']]

        # selected categories id's
        selected_categories_ids = [Category.objects.get(name=category).id for category in selected_categories]

        # sum of querysets for each category
        selected_categories_queryset = []

        for pk in selected_categories_ids:
            selected_categories_queryset.extend(
                Property.objects.filter(listing_status_id=selected_status_id, category_id=pk))

        # category slug and category name in tuple for response
        # -> [(category_slug, category_name), (category_slug, category_name), ...]
        selected_status_categories = sorted(list(set([(obj.category.slug, obj.category.name) for obj in
                                                      Property.objects.filter(listing_status_id=selected_status_id)])))

        # minimum & maximum price for filtering queryset by status and categories for response
        min_price = min([obj.price for obj in selected_categories_queryset]) if len(
            [obj.price for obj in selected_categories_queryset]) != 0 else min_price_of_selected_queryset
        max_price = max([obj.price for obj in selected_categories_queryset]) if len(
            [obj.price for obj in selected_categories_queryset]) != 0 else max_price_of_selected_queryset

        # selected price ranges
        selected_min_price_range = data['priceRange'][0]
        selected_max_price_range = data['priceRange'][1]

        # selected price ranges queryset
        selected_price_ranges_queryset = Property.objects.filter(
            pk__in={instance.id for instance in selected_categories_queryset},
            price__range=[selected_min_price_range, selected_max_price_range])

        number_of_bedrooms_selected_price_ranges_queryset = list(set([obj.number_of_bedrooms for obj in
                                                                      selected_price_ranges_queryset]))

        # selected minimum & maximum bedrooms
        selected_min_bedrooms = data['chosenMinBedrooms']
        max_bedrooms = []

        if len(selected_min_bedrooms) != 0:
            queryset = Property.objects.filter(pk__in={instance.id for instance in selected_price_ranges_queryset},
                                               number_of_bedrooms__gte=selected_min_bedrooms)

            for obj in queryset:
                max_bedrooms.append(obj.number_of_bedrooms)

        selected_max_bedrooms = data['chosenMaxBedrooms']

        # selected minimum & maximum bedrooms queryset
        selected_min_bedrooms_selected_queryset = []
        if len(selected_min_bedrooms) != 0 and len(selected_max_bedrooms) != 0:
            selected_min_bedrooms_selected_queryset.extend(Property.objects.filter(
                pk__in={instance.id for instance in selected_price_ranges_queryset},
                number_of_bedrooms__gte=int(selected_min_bedrooms)) & Property.objects.filter(
                pk__in={instance.id for instance in selected_price_ranges_queryset},
                number_of_bedrooms__lte=int(selected_max_bedrooms)))

        number_of_bathrooms_selected_price_ranges_queryset = list(set([obj.number_of_bathrooms for obj in
                                                                       selected_price_ranges_queryset]))

        selected_min_bathrooms = data['chosenMinBathrooms']
        max_bathrooms = []

        if len(selected_min_bathrooms) != 0:
            queryset = Property.objects.filter(pk__in={instance.id for instance in selected_price_ranges_queryset},
                                               number_of_bathrooms__gte=selected_min_bathrooms)

            for obj in queryset:
                max_bathrooms.append(obj.number_of_bathrooms)

        selected_max_bathrooms = data['chosenMaxBathrooms']

        # selected minimum & maximum bedrooms queryset
        if len(selected_min_bathrooms) != 0 and len(selected_max_bathrooms) != 0:
            selected_min_bedrooms_selected_queryset = []
            if len(selected_min_bedrooms) != 0 and len(selected_max_bedrooms) != 0:
                selected_min_bedrooms_selected_queryset.extend(Property.objects.filter(
                    pk__in={instance.id for instance in selected_price_ranges_queryset},
                    number_of_bedrooms__gte=int(selected_min_bedrooms)) & Property.objects.filter(
                    pk__in={instance.id for instance in selected_price_ranges_queryset},
                    number_of_bedrooms__lte=int(selected_max_bedrooms)))

        response.update(
            {
                'categories': selected_status_categories,
                'price_range': [min_price, max_price],
                'min_bedrooms': number_of_bedrooms_selected_price_ranges_queryset,
                'max_bedrooms': list(set(max_bedrooms)),
                'min_bathrooms': number_of_bathrooms_selected_price_ranges_queryset,
                'max_bathrooms': list(set(max_bathrooms)),
            }
        )

        return JsonResponse(data=response)


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
