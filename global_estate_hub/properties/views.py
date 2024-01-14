from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Property, City
from django.contrib.auth.decorators import login_required


def properties(request):
    queryset = []
    cities = sorted(list(set([city.name for city in City.objects.all()])))

    if request.method == 'GET':
        if request.GET:
            if 'properties-order' in request.GET:
                if request.GET.get('properties-order'):
                    request.session['sorted_type'] = request.GET.get('properties-order')

                    if 'Oldest Properties' in request.session['sorted_type']:
                        queryset.extend(Property.objects.all().order_by('date_posted'))

                    elif 'Alphabetically Ascending' in request.session['sorted_type']:
                        queryset.extend(Property.objects.all().order_by('title'))

                    elif 'Alphabetically Descending' in request.session['sorted_type']:
                        queryset.extend(Property.objects.all().order_by('-title'))

                    else:
                        queryset.extend(Property.objects.all().order_by('-date_posted'))

        else:
            request.session['sorted_type'] = 'Newest Properties'
            queryset.extend(Property.objects.all().order_by('-date_posted'))

    return render(request=request, template_name='properties/properties.html', context={
        'title': 'Properties',
        'properties': queryset,
        'cities': cities,
        'sorted_type': request.session['sorted_type'],
    })


def property_results(request):
    queryset = []
    cities = sorted(list(set([city.name for city in City.objects.all()])))

    if 'keyword' in request.GET:
        if request.GET.get('keyword'):
            request.session['keyword'] = request.GET.get('keyword')
            if 'properties-order' not in request.GET:
                request.session['sorted_type'] = 'Newest Properties'
                keyword = request.GET.get('keyword')

                queryset.extend(Property.objects.filter(title__icontains=keyword).order_by('-date_posted'))

    else:
        if 'properties-order' in request.GET:
            if request.GET.get('properties-order'):
                request.session['sorted_type'] = request.GET.get('properties-order')
                if request.session['keyword']:
                    keyword = request.session['keyword']
                    if 'Oldest Properties' in request.session['sorted_type']:
                        queryset.extend(Property.objects.filter(title__icontains=keyword).order_by('date_posted'))

                    elif 'Alphabetically Ascending' in request.session['sorted_type']:
                        queryset.extend(Property.objects.filter(title__icontains=keyword).order_by('title'))

                    elif 'Alphabetically Descending' in request.session['sorted_type']:
                        queryset.extend(Property.objects.filter(title__icontains=keyword).order_by('-title'))

                    else:
                        queryset.extend(Property.objects.filter(title__icontains=keyword).order_by('-date_posted'))

    return render(request=request, template_name='properties/property-results.html', context={
        'title': 'Property Results',
        'properties': queryset,
        'cities': cities,
        'sorted_type': request.session['sorted_type']
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
