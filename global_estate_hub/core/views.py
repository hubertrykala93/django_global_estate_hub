from django.shortcuts import render
from django.http import JsonResponse
from .models import Newsletter
import json
import re
from honeypot.decorators import check_honeypot


def index(request):
    return render(request=request, template_name='core/index.html', context={
        'title': 'Home',
    })


# @check_honeypot(field_name='checkbox')
def newsletter(request):
    data = json.loads(s=request.body.decode('utf-8'))
    print(data)
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))
        print(data)
        email = data['email']

        response = {
            "valid":
                False if not email else
                False if not re.match(pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$', string=email) else
                False if re.match(pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$',
                                  string=email) and Newsletter.objects.filter(email=email).exists() else
                True,
            "message":
                "The email field cannot be empty." if not email else
                "The e-mail address format is invalid." if not re.match(
                    pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$', string=email) else
                f"The e-mail address {email} already exists." if re.match(
                    pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$',
                    string=email) and Newsletter.objects.filter(
                    email=email).exists() else
                "",
        }

        print(response)

        # if response[0]['valid'] is True and response[1]['valid'] is False:
        #     new_subscriber = Newsletter(email=email)
        #     new_subscriber.save()

        return JsonResponse(data=response, safe=False)


def about(request):
    return render(request=request, template_name='core/about.html', context={
        'title': 'About',
    })


def properties(request):
    return render(request=request, template_name='core/properties.html', context={
        'title': 'Properties',
    })


def faq(request):
    return render(request=request, template_name='core/faq.html', context={
        'title': 'Faq',
    })


def pages(request):
    return render(request=request, template_name='core/pages.html', context={
        'title': 'Pages',
    })


def contact(request):
    return render(request=request, template_name='core/contact.html', context={
        'title': 'Contact',
    })


def error(request):
    return render(request=request, template_name='core/error.html', context={
        'title': 'Error 404',
    })
