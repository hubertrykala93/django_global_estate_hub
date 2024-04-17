import django.http.response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Newsletter, ContactMail
import json
import re
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os
from dotenv import load_dotenv
from django.utils.html import strip_tags
from properties.models import Property, City, Category, ListingStatus
from blog.models import Article
from properties.views import property_pagination
import datetime
from accounts.models import User
from django.db.models import Count

load_dotenv()


def index(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the homepage template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    if request.session.get('filters'):
        request.session.pop('filters')

    latest_articles = Article.objects.all().order_by('-date_posted')[:3]
    latest_properties = Property.objects.all().order_by('-date_posted')[:3]
    cities = sorted(
        set([obj.city for obj in Property.objects.filter(listing_status=ListingStatus.objects.get(name='Rent'))]),
        key=lambda x: x.name)
    categories = sorted(set([obj.category for obj in
                             Property.objects.filter(listing_status=ListingStatus.objects.get(name='Rent'))]),
                        key=lambda x: x.name)
    years_of_built = Property.objects.filter(
        listing_status_id=ListingStatus.objects.get(name='Rent')).values_list('year_of_built', flat=True).order_by(
        'year_of_built').distinct()
    agents = User.objects.annotate(property_count=Count('properties')).order_by('-property_count')[:3]

    # year counter
    project_started = 2020
    current_year = datetime.date.today().year
    substracted_year = current_year - project_started

    # customers counter
    substracted_customers_counter = len(list(
        set([obj.purchasing_user for obj in Property.objects.all() if obj.purchasing_user is not None]))) - 1 if len(
        list(set([obj.purchasing_user for obj in Property.objects.all() if
                  obj.purchasing_user is not None]))) > 1 else len(
        list(set([obj.purchasing_user for obj in Property.objects.all() if obj.purchasing_user is not None])))
    customers_counter = len(
        list(set([obj.purchasing_user for obj in Property.objects.all() if obj.purchasing_user is not None])))

    # properties counter
    substracted_properties_counter = Property.objects.all().count() - 1 if len(
        Property.objects.all()) > 1 else Property.objects.all().count()
    properties_counter = Property.objects.all().count()

    return render(request=request, template_name='core/index.html', context={
        'title': 'Home',
        'latest_articles': latest_articles,
        'latest_properties': latest_properties,
        'project_started': project_started,
        'substracted_year': substracted_year,
        'substracted_customers_counter': substracted_customers_counter,
        'customers_counter': customers_counter,
        'substracted_properties_counter': substracted_properties_counter,
        'properties_counter': properties_counter,
        'cities': cities,
        'categories': categories,
        'years_of_built': years_of_built,
        'agents': agents,
    })


def top_agents(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the top agents template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    agents = User.objects.annotate(property_count=Count('properties')).order_by('-property_count')

    return render(request=request, template_name='core/top-agents.html', context={
        'title': 'Top Agents',
        'agents': agents,
    })


def newsletter(request) -> django.http.response.JsonResponse:
    """
    The function handling the form for saving an email address for the newsletter to the database
    using the POST method with Asynchronous JavaScript and XMLHttpRequest (AJAX) request.
    Upon successful form validation, an email message is automatically sent
    from the website administrator to the provided email address.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        email, spam_verification = [data[key] for key in data.keys()]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
                "message": "",
            })

        response = {
            "valid":
                False if not email else
                False if not re.match(pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                      string=email) else
                False if re.match(pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                  string=email) and Newsletter.objects.filter(email=email).exists() else
                True,
            "message":
                "The email field cannot be empty." if not email else
                "The e-mail address format is invalid." if not re.match(
                    pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', string=email) else
                f"The e-mail address {email} already exists." if re.match(
                    pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                    string=email) and Newsletter.objects.filter(
                    email=email).exists() else
                "Congratulations! You have successfully subscribed to our newsletter.",
        }

        if response['valid']:
            new_subscriber = Newsletter(email=email)
            new_subscriber.save()

            try:
                html_message = render_to_string(template_name='core/newsletter_mail.html', context={
                    'email': email,
                })
                plain_message = strip_tags(html_message)

                message = EmailMultiAlternatives(
                    subject='Thank you for subscribing to our newsletter!',
                    body=plain_message,
                    from_email=os.environ.get("EMAIL_HOST_USER"),
                    to=[email],
                )

                message.attach_alternative(content=html_message, mimetype='text/html')
                message.send(fail_silently=True)

                return JsonResponse(data=response)

            except Exception:
                return JsonResponse(data={
                    "valid": False,
                    "message": "Unfortunately, we were unable to sign up your email for our newsletter. "
                               "Please try again.",
                })

        else:
            return JsonResponse(data=response)


def about(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the about template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    return render(request=request, template_name='core/about.html', context={
        'title': 'About',
    })


def faq(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the FAQ template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    return render(request=request, template_name='core/faq.html', context={
        'title': 'Faq',
    })


def contact(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the contact template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    return render(request=request, template_name='core/contact.html', context={
        'title': 'Contact',
    })


def error(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the error404 template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    return render(request=request, template_name='core/error.html', context={
        'title': 'Error 404',
    })


def send_message(request) -> django.http.response.JsonResponse:
    """
    The function handling the form for sending an email message to the website administrator
    using the POST method with Asynchronous JavaScript and XMLHttpRequest (AJAX) request.
    The function also saves data such as Full Name, Phone Number, Email Address, and Message to the database.
    Upon successful form validation, an email message is automatically sent to the website administrator.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        fullname, phone_number, email, content = [data[key][0] for key in list(data.keys())[:-1]]
        spam_verification = [data[key] for key in data][-1]
        fullname_field, phone_field, email_field, content_field = [data[key][1] for key in list(data.keys())[:-1]]
        fullname_label, phone_label, email_label, content_label = [data[key][2] for key in list(data.keys())[:-1]]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
            }, safe=False)

        response = [
            {
                "valid":
                    False if not fullname else
                    True,
                "field": fullname_field,
                "message":
                    f"The {fullname_label} field cannot be empty." if not fullname else
                    "",
            },
            {
                "valid":
                    False if not phone_number else
                    False if not re.match(pattern="^\\+?[1-9][0-9]{7,14}$",
                                          string=phone_number) else
                    True,
                "field": phone_field,
                "message":
                    f"The {phone_label} field cannot be empty." if not phone_number else
                    f"The {phone_label} format is invalid." if not re.match(
                        pattern="^\\+?[1-9][0-9]{7,14}$",
                        string=phone_number) else
                    "",
            },
            {
                "valid":
                    False if not email else
                    False if not re.match(pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                          string=email) else
                    True,
                "field": email_field,
                "message":
                    f"The {email_label} field cannot be empty." if not email else
                    f"The {email_label} format is invalid." if not re.match(
                        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', string=email) else
                    "",
            },
            {
                "valid":
                    False if not content else
                    True,
                "field": content_field,
                "message":
                    f"The {content_label} field cannot be empty." if not content else
                    "",
            }
        ]

        validation = list(set([data['valid'] for data in response]))

        if len(validation) == 1:
            if validation[0]:
                new_mail = ContactMail(full_name=fullname, phone_number=phone_number, email=email, content=content)
                new_mail.save()

                try:
                    html_message = render_to_string(template_name='core/contact_mail.html', context={
                        'fullname': fullname,
                        'phone_number': phone_number,
                        'email': email,
                        'content': content,
                    })
                    plain_message = strip_tags(html_message)

                    message = EmailMultiAlternatives(
                        subject=f"E-mail from Global Estate Hub.",
                        body=plain_message,
                        from_email=os.environ.get("EMAIL_HOST_USER"),
                        to=[os.environ.get("EMAIL_HOST_USER")],
                        headers={'Reply-To': email},
                    )

                    message.attach_alternative(content=html_message, mimetype='text/html')
                    message.send(fail_silently=True)

                    return JsonResponse(data=response, safe=False)

                except Exception:
                    return JsonResponse(data={
                        "valid": False,
                        "message": "The message could not be sent."
                    }, safe=False)

            else:
                return JsonResponse(data=response, safe=False)

        else:
            return JsonResponse(data=response, safe=False)


def properties_results(request) -> django.http.response.JsonResponse or django.http.response.HttpResponse:
    """
    A function handling two request methods, POST and GET. During a POST request, the function handles
    a property search form using fields in the database such as listing_status, city, category, and year_of_built
    with the help of Asynchronous JavaScript and XMLHttpRequest (AJAX).
    The function returns a JsonResponse with updated city, category, and year_of_built fields
    depending on the listing_status chosen by the user during the POST method.
    It also saves the filters selected by the user in the session.

    During a GET request, the filters selected by the user in the session are unpacked,
    and a queryset of properties is rendered based on these filters.
    The user also has the option to sort the search results.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse or django.http.response.HttpResponse
    """
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))
        filters = {}
        response = {}

        if 'chosenStatus' in data or 'chosenLocation' in data or 'chosenCategory' in data or 'chosenYear' in data:
            if len(data['chosenStatus']) != 0:
                filters['listing_status_id'] = ListingStatus.objects.get(
                    slug='-'.join(data['chosenStatus'].lower().split())).id
                request.session['filters'] = filters

                response.update(
                    {
                        'chosenStatus': list(
                            ListingStatus.objects.values_list('name', flat=True).order_by('name').distinct()),
                        'chosenLocation': list(Property.objects.filter(**filters).values_list('city__name',
                                                                                              flat=True).order_by(
                            'city__name').distinct()),
                        'chosenCategory': list(Property.objects.filter(**filters).values_list('category__name',
                                                                                              flat=True).order_by(
                            'category__name').distinct()),
                        'chosenYear': list(Property.objects.filter(**filters).values_list('year_of_built',
                                                                                          flat=True).order_by(
                            'year_of_built').distinct()),
                    }
                )

            if len(data['chosenLocation']) != 0:
                filters['city_id'] = City.objects.get(slug='-'.join(data['chosenLocation'].lower().split())).id
                request.session['filters'] = filters

            if len(data['chosenCategory']) != 0:
                filters['category_id'] = Category.objects.get(slug='-'.join(data['chosenCategory'].lower().split())).id
                request.session['filters'] = filters

            if len(data['chosenYear']) != 0:
                filters['year_of_built'] = int(data['chosenYear'])
                request.session['filters'] = filters

            return JsonResponse(data=response)

    elif request.method == 'GET':
        queryset = []
        request.session['sorted_type'] = 'Newest Properties'

        if 'properties-order' in request.GET:
            if 'filters' in request.session:
                if 'Newest Properties' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = 'Newest Properties'
                    queryset.extend(Property.objects.filter(**request.session['filters']).order_by('-date_posted'))

                elif 'Oldest Properties' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = 'Oldest Properties'
                    queryset.extend(Property.objects.filter(**request.session['filters']).order_by('date_posted'))

                elif 'Price Ascending' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = 'Price Ascending'
                    queryset.extend(Property.objects.filter(**request.session['filters']).order_by('price'))

                elif 'Price Descending' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = 'Price Descending'
                    queryset.extend(Property.objects.filter(**request.session['filters']).order_by('-price'))

                elif 'Featured' in request.GET.get('properties-order'):
                    request.session['sorted_type'] = 'Featured'
                    queryset.extend(Property.objects.filter(**request.session['filters']).order_by('-is_featured'))

        else:
            if 'filters' in request.session:
                request.session['sorted_type'] = 'Newest Properties'
                queryset.extend(Property.objects.filter(**request.session['filters']).order_by('-date_posted'))

            else:
                request.session['sorted_type'] = 'Newest Properties'
                request.session['filters'] = {
                    'listing_status_id': ListingStatus.objects.get(slug='rent').id
                }
                queryset.extend(Property.objects.filter(**request.session['filters']).order_by('-date_posted'))

        return render(request=request, template_name='core/properties-results.html', context={
            'title': 'Properties Results',
            'properties': queryset,
            'sorted_type': request.session['sorted_type'],
            'pages': property_pagination(request=request, object_list=queryset, per_page=6),
        })


def rodo_rules(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the rodo rules template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    email = os.environ.get('EMAIL_FROM')

    return render(request=request, template_name='core/rodo-rules.html', context={
        'title': 'Rodo Rules',
        'email': email,
    })


def privacy_policy(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the privacy policy template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    email = os.environ.get('EMAIL_FROM')

    return render(request=request, template_name='core/privacy-policy.html', context={
        'title': 'Privacy Policy',
        'email': email,
    })
