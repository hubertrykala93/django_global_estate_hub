from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def index(request):
    return render(request=request, template_name='estates/index.html', context={
        'title': 'Home',
    })


def category(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        print(name)

        return JsonResponse(data={
            "category": name,
        })

    else:
        name = request.POST.get('name', None)

        return JsonResponse(data={
            "category": name,
        })
