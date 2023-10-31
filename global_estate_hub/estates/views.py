from django.shortcuts import render


def index(request):
    return render(request=request, template_name='estates/index.html', context={
        'title': 'Home',
    })


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


def estate(request):
    return render(request=request, template_name='estates/estate-details.html', context={
        'title': 'Estate Details',
    })


def detail(request):
    return render(request=request, template_name='estates/detail.html', context={
        'title': 'Detail',
    })
