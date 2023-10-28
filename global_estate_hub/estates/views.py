from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def index(request):
    return render(request=request, template_name='estates/index.html', context={
        'title': 'Home',
    })


@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        category = request.POST.get('category', None)
        print('POST')
        print(category)

        return JsonResponse(data={
            "category": category,
        })

    else:
        category = request.GET.get('category', None)
        print('GET')
        print(category)

        return JsonResponse(data={
            "category": category,
        })
