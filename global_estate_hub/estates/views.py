from django.shortcuts import render
from django.conf import settings


def index(request):
    return render(request=request, template_name='estates/index.html', context={
        'title': 'Home',
    })
