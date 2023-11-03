from django.shortcuts import render
from django.http import JsonResponse
from .models import Newsletter
import json


def index(request):
    return render(request=request, template_name='estates/index.html', context={
        'title': 'Home',
    })


def newsletter(request):
    if request.method == 'POST':
        email = json.loads(s=request.body.decode('utf-8'))['email']
        print(f"Request Body -> {request.body}")
        print()
        print(f"Request.POST -> {request.POST}")
        print()
        print(f"Request Body Decoded -> {request.body.decode('utf-8')}")
        print()
        print(email)

        if email is not None and len(email) == 0:
            return JsonResponse(data={
                "valid": False,
                "message": "The email address cannot be empty.",
            })

        elif Newsletter.objects.filter(email=email).exists():
            return JsonResponse(data={
                "valid": False,
                "message": "The email address already exists.",
            })

        elif email is None:
            return JsonResponse(data={
                "valid": False,
                "message": "The email address is None.",
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
            "message": "The email address was not added.",
        })


# @csrf_exempt
# def newsletter(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#
#         if email is not None and len(email) == 0:
#             return JsonResponse(data={
#                 "valid": False,
#                 "message": "The email address cannot be empty.",
#             })
#
#         elif Newsletter.objects.filter(email=email).exists():
#             return JsonResponse(data={
#                 "valid": False,
#                 "message": "The email address already exists.",
#             })
#
#         elif email is None:
#             return JsonResponse(data={
#                 "valid": False,
#                 "message": "The email address is None.",
#             })
#
#         else:
#             new_subscriber = Newsletter(email=email)
#             new_subscriber.save()
#
#             return JsonResponse(data={
#                 "valid": True,
#                 "message": "Congratulations! You have subscribed to our newsletter.",
#             })
#
#     else:
#         return JsonResponse(data={
#             "valid": False,
#             "message": "The email address was not added.",
#         })


def about(request):
    return render(request=request, template_name='estates/about.html', context={
        'title': 'About',
    })


def properties(request):
    return render(request=request, template_name='estates/properties.html', context={
        'title': 'Properties',
    })


def blog(request):
    return render(request=request, template_name='estates/blog.html', context={
        'title': 'Blog',
    })


def pages(request):
    return render(request=request, template_name='estates/pages.html', context={
        'title': 'Pages',
    })


def contact(request):
    return render(request=request, template_name='estates/contact.html', context={
        'title': 'Contact',
    })
