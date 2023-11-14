from django.shortcuts import render
from django.http import JsonResponse
from .models import Newsletter
import json
import re
from blog.models import Article


def index(request):
    articles = Article.objects.order_by('-date_posted')[:3]

    return render(request=request, template_name='core/index.html', context={
        'title': 'Home',
        'articles': articles,
    })


def newsletter(request):
    if request.method == 'POST':
        email = json.loads(s=request.body.decode('utf-8'))['email']

        if not email:
            return JsonResponse(data={
                "valid": False,
                "message": "The email address cannot be empty.",
            })

        else:
            if re.match(pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$', string=email):
                if Newsletter.objects.filter(email=email).exists():
                    return JsonResponse(data={
                        "valid": False,
                        "message": "The email address already exists.",
                    })

                else:
                    new_subscriber = Newsletter(email=email)
                    new_subscriber.save()

                    return JsonResponse(data={
                        "valid": True,
                        "message": "Congratulations! You have subscribed to our newsletter.",
                    })

            else:
                return JsonResponse(data={
                    "valid": False,
                    "message": "Invalid email address format.",
                })

    else:
        return JsonResponse(data={
            "valid": False,
            "message": "The email address was not added.",
        })


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
