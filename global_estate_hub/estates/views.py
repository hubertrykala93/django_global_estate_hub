from django.shortcuts import render


def index(request):
    return render(request=request, template_name='estates/index.html', context={
        'title': 'Home',
    })
