from django.shortcuts import render


def index(request):
    return render(request=request, template_name='estates/index.html', context={
        'title': 'Home',
    })


def about(request):
    # print(f"Path -> '{request.path}'")
    # print(f"Scheme -> '{request.scheme}'")
    # print(f"Body -> '{request.body}'")
    # print(f"Path Info -> '{request.path_info}'")
    # print(f"Method -> '{request.method}'")
    # print(f"Encoding -> '{request.encoding}'")
    # print(f"Content Type -> '{request.content_type}'")
    # print(f"Content Params -> '{request.content_params}'")
    # print(f"GET -> '{request.GET}'")
    # print(f"POST -> '{request.POST}'")
    # print(f"Cookies -> '{request.COOKIES}'")
    # print(f"Files -> '{request.FILES}'")
    # print(f"Meta -> '{request.META}'")
    # print(f"Header -> '{request.headers['Accept-Encoding']}'")
    # print(f"Session -> '{request.session.__dict__}'")
    # print(f"User -> '{request.user}'")
    # print(f"Get Host -> '{request.get_host()}'")
    # print(f"Get Port -> '{request.get_port()}'")
    # print(f"Build Absolute Uri -> '{request.build_absolute_uri()}'")
    # print(f"Is Secure -> '{request.is_secure()}'")
    # print(f"Accepts -> '{request.accepts(media_type=request.content_type)}'")
    # print(request.user.is_authenticated)

    return render(request=request, template_name='estates/about.html', context={
        'title': 'About',
    })


def properties(request):
    return render(request=request, template_name='estates/properties.html', context={
        'title': 'Properties',
    })


def pages(request):
    return render(request=request, template_name='estates/pages.html', context={
        'title': 'Pages',
    })


def blogs(request):
    return render(request=request, template_name='estates/blogs.html', context={
        'title': 'Blogs',
    })


def contact(request):
    return render(request=request, template_name='estates/contact.html', context={
        'title': 'Contact',
    })


def add_category(request):
    pass
