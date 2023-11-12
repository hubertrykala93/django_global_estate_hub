from django.shortcuts import render


def blog(request):
    return render(request=request, template_name='blog/blog.html', context={
        'title': 'Blog',
    })
