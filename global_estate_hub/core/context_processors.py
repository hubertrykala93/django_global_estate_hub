from django.middleware.csrf import get_token


def breadcrumbs_urls(request):
    return {
        'breadcrumbs_urls': request.path.split('/')[1:],
    }


def generate_token(request):
    return {
        'csrf_token': get_token(request=request)
    }


# def breadcrumbs_urls(path):
#     return {
#         'breadcrumbs_urls': path.split('/')[1:],
#     }


# path = '/blog/buys/choosing-the-perfect-family-house'
# urls = breadcrumbs_urls(path=path)['breadcrumbs_urls']
#
# paths = []
