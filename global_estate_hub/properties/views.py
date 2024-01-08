from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Property


def add_property(request):
    return render(request=request, template_name='properties/add-property.html', context={
        'title': 'Add Property',
    })


def add_to_favourites(request):
    if request.method == 'PATCH':
        property_id = int(json.loads(s=request.body.decode('utf-8'))['propertyId'])
        property = Property.objects.get(id=property_id)

        if request.user in property.favourites.all():
            return JsonResponse(data={
                "valid": False
            })

        else:
            property.favourites.add(request.user)
            property.save()

            return JsonResponse(data={
                "valid": True,
                "propertyId": property_id,
            })
