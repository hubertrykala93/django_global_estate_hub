from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request=request, template_name='estates/index.html', context={
        'title': 'Home',
    })


def get_request(request):
    return HttpResponse(content="GET request received successfully.")


def post_request(request):
    print(request.POST)
    print(request.POST.get('name'))
    print(request.POST.get('age'))
    return HttpResponse(content="POST request received successfully.")


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
