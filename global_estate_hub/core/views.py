from django.shortcuts import render
from django.http import JsonResponse
from .models import Newsletter
import json
import re


def index(request):
    return render(request=request, template_name='core/index.html', context={
        'title': 'Home',
    })


def newsletter(request):
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))
        email = data['email']
        spam_verification = data['url']
        # spam_verification = spam_verification + '123'

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": -1,
                "message": "",
            })

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
                "Congratulations! You have successfully subscribed to our newsletter.",
        }

        if response['valid'] is True:
            new_subscriber = Newsletter(email=email)
            new_subscriber.save()

            return JsonResponse(data=response)

        else:
            return JsonResponse(data=response)


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
