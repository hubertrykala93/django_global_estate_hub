from django.middleware.csrf import get_token


def breadcrumbs_urls(request):
    return {
        'breadcrumbs_urls': request.path.split('/')[1:],
    }


def generate_token(request):
    return {
        'csrf_token': get_token(request=request)
    }
