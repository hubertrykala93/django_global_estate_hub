from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Newsletter
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token


def index(request):
    return render(request=request, template_name='estates/index.html', context={
        'title': 'Home',
    })


@csrf_exempt
def newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)

        new_subscriber = Newsletter(email=email)
        new_subscriber.save()

        return JsonResponse(data={
            "valid": True,
            "message": "Your e-mail address was added.",
        })

    elif request.method == 'GET':
        email = request.GET.get('email')
        print(email)

        return JsonResponse(data={
            "valid": False,
            "message": "Your e-mail address wasn't added.",
        })


# def get_request(request):
#     print(request.GET)
#     return HttpResponse(content="GET request received successfully.")
#
#
# def post_request(request):
#     print(request.POST)
#     print(request.POST.get('name'))
#     print(request.POST.get('age'))
#
#     return JsonResponse(data={
#         'name': request.POST.get('name'),
#         'age': request.POST.get('age'),
#     })

# return HttpResponse(content="POST request received successfully.")


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
