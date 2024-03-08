from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
import re
import os
from accounts.models import User
from .models import Property, ListingStatus, Category, City, Review
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages


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
        'listing_statuses': sorted(set([obj.name for obj in ListingStatus.objects.all()])),
        'categories': sorted(set([obj.name for obj in Category.objects.all()])),
        'min_price': min(set([obj.price for obj in Property.objects.all()])),
        'max_price': max(set([obj.price for obj in Property.objects.all()])),
        'number_of_bedrooms': sorted(set([obj.number_of_bedrooms for obj in Property.objects.all()])),
        'number_of_bathrooms': sorted(set([obj.number_of_bathrooms for obj in Property.objects.all()])),
        'cities': sorted(set([obj.name for obj in City.objects.all()])),
        'square_meters': sorted(set([obj.square_meters for obj in Property.objects.all()]))
    }


def properties(request):
    queryset = []
    context = {}
    filters = {}

    if request.GET:
        print('Request GET.')
        if 'properties-order' in request.GET:
            print('If properties order in request GET.')
            if 'keyword' in request.session:
                print('Keyword in request session.')
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
                    queryset.clear()
                    request.session['sorted_type'] = 'Newest Properties'
                    queryset.extend(Property.objects.filter(title__icontains=request.session.get('keyword')).order_by(
                        '-date_posted'))

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
            request.session['sorted_type'] = 'Newest Properties'
            request.session['keyword'] = request.GET.get('keyword')
            keyword = request.GET.get('keyword')
            queryset.clear()
            queryset.extend(
                Property.objects.filter(title__icontains=keyword).order_by('-date_posted'))

        # elif 'status' or 'category' or 'min_price' or 'max_price' or 'min_bedrooms' or 'max_bedrooms' or 'min_bathrooms' or 'max_bathrooms' or 'location' or 'min_square' or 'max_square' in request.GET:
        #     if 'status' in request.GET:
        #         print('Listing Status in request GET.')
        #         filters['listing_status_id'] = ListingStatus.objects.get(
        #             slug='-'.join(request.GET.get('status').lower().split())).id
        #
        #         request.session['filters'] = filters
        #
        #         queryset.clear()
        #         queryset.extend(Property.objects.filter(**filters))
        #
        #     if 'category' in request.GET:
        #         print('Category in request GET.')
        #         if len(request.GET.getlist('category')) == 1:
        #             print('Category length is equal to 1.')
        #             filters['category_id'] = Category.objects.get(
        #                 slug='-'.join(request.GET.get('category').lower().split())).id
        #
        #             request.session['filters'] = filters
        #
        #             queryset.clear()
        #             queryset.extend(Property.objects.filter(**filters))
        #
        #         else:
        #             print('Category length is more than 1.')
        #             filters['category__pk__in'] = [Category.objects.get(slug=obj).id for obj in
        #                                            request.GET.getlist('category')]
        #
        #             request.session['filters'] = filters
        #
        #             queryset.clear()
        #             queryset.extend(Property.objects.filter(**filters))
        #
        #     if 'min_price' and 'max_price' in request.GET:
        #         print('Min Price and Max Price in request GET.')
        #         filters['price__range'] = [int(request.GET.get('min_price')), int(request.GET.get('max_price'))]
        #
        #         request.session['filters'] = filters
        #
        #         queryset.clear()
        #         queryset.extend(Property.objects.filter(**filters))
        #
        #     if 'min_bedrooms' in request.GET:
        #         print('Min Bedrooms in request GET.')
        #
        #         if 'max_bedrooms' in request.GET:
        #             print('Max Bedrooms in request GET.')
        #
        #             if request.GET.get('min_bedrooms') > request.GET.get('max_bedrooms'):
        #                 print('Min Bedrooms more than Max Bedrooms.')
        #                 messages.info(request=request,
        #                               message='The maximum number of bedrooms cannot be less than the minimum number of bedrooms.')
        #                 return redirect(to='properties')
        #
        #             else:
        #                 print('Min Bedrooms less or equal than Max Bedrooms.')
        #                 filters['number_of_bedrooms__range'] = [int(request.GET.get('min_bedrooms')),
        #                                                         int(request.GET.get('max_bedrooms'))]
        #
        #                 request.session['filters'] = filters
        #
        #                 queryset.clear()
        #                 queryset.extend(Property.objects.filter(**filters))
        #
        #         else:
        #             print('Min Bedrooms and not Max Bedrooms.')
        #             filters['number_of_bedrooms__range'] = [int(request.GET.get('min_bedrooms')), int(max(
        #                 sorted(set([obj.number_of_bedrooms for obj in Property.objects.all()]))))]
        #
        #             request.session['filters'] = filters
        #
        #             queryset.clear()
        #             queryset.extend(Property.objects.filter(**filters))
        #
        #     if 'max_bedrooms' in request.GET:
        #         print('Max Bedrooms in request GET.')
        #
        #         if 'min_bedrooms' in request.GET:
        #             print('Min Bedrooms in request GET.')
        #
        #             if request.GET.get('min_bedrooms') > request.GET.get('max_bedrooms'):
        #                 print('Min Bedrooms more than Max Bedrooms.')
        #                 messages.info(request=request,
        #                               message='The minimum number of bedrooms cannot be greater than the maximum number of bedrooms.')
        #                 return redirect(to='properties')
        #
        #             else:
        #                 print('Min Bedrooms less than Max Bedrooms.')
        #                 filters['number_of_bedrooms__range'] = [int(request.GET.get('min_bedrooms')),
        #                                                         int(request.GET.get('max_bedrooms'))]
        #
        #                 request.session['filters'] = filters
        #
        #                 queryset.clear()
        #                 queryset.extend(Property.objects.filter(**filters))
        #
        #         else:
        #             print('Max Bedrooms and not Min Bedrooms.')
        #             filters['number_of_bedrooms__range'] = [
        #                 int(min(sorted(set([obj.number_of_bedrooms for obj in Property.objects.all()])))),
        #                 request.GET.get('max_bedrooms')]
        #
        #             request.session['filters'] = filters
        #
        #             queryset.clear()
        #             queryset.extend(Property.objects.filter(**filters))
        #
        #     if 'min_bathrooms' in request.GET:
        #         print('Min Bathrooms in request GET.')
        #
        #         if 'max_bathrooms' in request.GET:
        #             print('If Min Bathrooms and Max Bathrooms in request GET.')
        #
        #             if request.GET.get('min_bathrooms') > request.GET.get('max_bathrooms'):
        #                 print('Min Bathrooms more than Max Bathrooms.')
        #                 messages.info(request=request,
        #                               message='The maximum number of bathrooms cannot be less than the minimum number of bathrooms.')
        #                 return redirect(to='properties')
        #
        #             else:
        #                 print('Min Bathrooms less than Max Bathrooms.')
        #                 filters['number_of_bathrooms__range'] = [int(request.GET.get('min_bathrooms')),
        #                                                          int(request.GET.get('max_bathrooms'))]
        #
        #                 request.session['filters'] = filters
        #
        #                 queryset.clear()
        #                 queryset.extend(Property.objects.filter(**filters))
        #
        #         else:
        #             print('Min Bathrooms in request GET and not Max Bathrooms in request GET.')
        #             filters['number_of_bathrooms__range'] = [int(request.GET.get('min_bathrooms')), int(max(
        #                 sorted(set([obj.number_of_bathrooms for obj in Property.objects.all()]))))]
        #
        #             request.session['filters'] = filters
        #
        #             queryset.clear()
        #             queryset.extend(Property.objects.filter(**filters))
        #
        #     if 'max_bathrooms' in request.GET:
        #         print('Max Bathrooms in request GET.')
        #
        #         if 'min_bathrooms' in request.GET:
        #             print('Max Bathrooms and Min Bathrooms in request GET.')
        #
        #             if request.GET.get('max_bathrooms') < request.GET.get('min_bathrooms'):
        #                 messages.info(request=request,
        #                               message='The minimum number of bathrooms cannot be greater than the maximum number of bathrooms.')
        #                 return redirect(to='properties')
        #
        #             else:
        #                 print('Max Bathrooms greater than Min Bathrooms.')
        #                 filters['number_of_bathrooms__range'] = [int(request.GET.get('min_bathrooms')),
        #                                                          int(request.GET.get('max_bathrooms'))]
        #
        #                 request.session['filters'] = filters
        #
        #                 queryset.clear()
        #                 queryset.extend(Property.objects.filter(**filters))
        #
        #         else:
        #             print('Max Bathrooms in request GET and not Min Bathrooms in request GET.')
        #             filters['number_of_bathrooms__range'] = [
        #                 int(min(sorted(set([obj.number_of_bathrooms for obj in Property.objects.all()])))),
        #                 int(request.GET.get('max_bathrooms'))]
        #
        #             request.session['filters'] = filters
        #
        #             queryset.clear()
        #             queryset.extend(Property.objects.filter(**filters))
        #
        #     if 'location' in request.GET:
        #         filters['city__id'] = City.objects.get(slug='-'.join(request.GET.get('location').lower().split())).id
        #
        #         request.session['filters'] = filters
        #
        #         queryset.clear()
        #         queryset.extend(Property.objects.filter(**filters))
        #
        #     if 'min_square' in request.GET:
        #         print('Min Square in request GET.')
        #
        #         if 'max_square' in request.GET:
        #             print('Min Square and Max Square in request GET.')
        #
        #             if request.GET.get('min_square') > request.GET.get('max_square'):
        #                 print('Min Square greater than Max Square.')
        #                 messages.info(request=request,
        #                               message='The minimum square meters cannot be greater than the maximum square meters.')
        #                 return redirect(to='properties')
        #
        #             else:
        #                 print('Min Square Meters less than Max Square Meters.')
        #                 filters['square_meters__range'] = [float(request.GET.get('min_square')),
        #                                                    float(request.GET.get('max_square'))]
        #
        #                 request.session['filters'] = filters
        #
        #                 queryset.clear()
        #                 queryset.extend(Property.objects.filter(**filters))
        #
        #         else:
        #             print('Min Square in request GET and not Max Square in request GET.')
        #             filters['square_meters__range'] = [float(request.GET.get('min_square')), float(
        #                 max(sorted(set([obj.square_meters for obj in Property.objects.all()]))))]
        #
        #             request.session['filters'] = filters
        #
        #             queryset.clear()
        #             queryset.extend(Property.objects.filter(**filters))
        #
        #     if 'max_square' in request.GET:
        #         print('Max Square in request GET.')
        #
        #         if 'min_square' in request.GET:
        #             print('Max Square and Min Square in request GET.')
        #
        #             if request.GET.get('max_square') < request.GET.get('min_square'):
        #                 print('Max Square less than Min Square.')
        #                 messages.info(request=request,
        #                               message='The maximum square meters cannot be less than the minimum square meters.')
        #                 return redirect(to='properties')
        #
        #             else:
        #                 print('Max Square greater than Min Square.')
        #                 filters['square_meters__range'] = [float(request.GET.get('min_square')),
        #                                                    float(request.GET.get('max_square'))]
        #
        #                 request.session['filters'] = filters
        #
        #                 queryset.clear()
        #                 queryset.extend(Property.objects.filter(**filters))
        #
        #         else:
        #             print('Max Square in request GET and not Min Square in request GET.')
        #             filters['square_meters__range'] = [
        #                 float(min(sorted(set([obj.square_meters for obj in Property.objects.all()])))),
        #                 float(request.GET.get('max_square'))]
        #
        #             request.session['filters'] = filters
        #
        #             queryset.clear()
        #             queryset.extend(Property.objects.filter(**filters))

        else:
            print('No properties order, keyword and status in request GET.')
            request.session.get('sorted_type')
            request.session.pop('sorted_type')

            request.session['sorted_type'] = 'Newest Properties'
            queryset.extend(Property.objects.all().order_by('-date_posted'))

    else:
        print('No request GET.')
        if request.session.get('sorted_type'):
            request.session.pop('sorted_type')

        if request.session.get('keyword'):
            request.session.pop('keyword')

        request.session['sorted_type'] = 'Newest Properties'
        queryset.extend(Property.objects.all().order_by('-date_posted'))

        context.update({
            'listing_statuses': [obj.name for obj in ListingStatus.objects.all()],
            'categories': sorted(set([obj.category.name for obj in Property.objects.all()])),
            'min_price': min(list(set([obj.price for obj in Property.objects.all()]))),
            'max_price': max(list(set([obj.price for obj in Property.objects.all()]))),
            'number_of_bedrooms': sorted(set([obj.number_of_bedrooms for obj in Property.objects.all()])),
            'number_of_bathrooms': sorted(set([obj.number_of_bathrooms for obj in Property.objects.all()])),
            'cities': sorted(set([obj.name for obj in City.objects.all()])),
            'square_meters': sorted(set([obj.square_meters for obj in Property.objects.all()])),
        })

    context.update({
        'title': 'Properties',
        'properties': len(queryset),
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
    city = City.objects.get(name=property_obj.city)
    reviews = Review.objects.filter(property_id=property_obj.id)

    images = enumerate([
        '/media/property_images/photo_1.jpg',
        '/media/property_images/photo_2.jpg',
        '/media/property_images/photo_3.jpg',
        '/media/property_images/photo_4.jpg',
        '/media/property_images/photo_5.jpg',
        '/media/property_images/photo_6.jpg',
    ])

    return render(request=request, template_name='properties/property-details.html', context={
        'title': property_obj.title,
        'property': property_obj,
        'city': city,
        'images': images,
        'range': range(5),
        'reviews': reviews,
    })


def add_review(request, category_slug, property_slug):
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


def schedule_tour(request, category_slug, property_slug):
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
                message.send(fail_silently=True)

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

