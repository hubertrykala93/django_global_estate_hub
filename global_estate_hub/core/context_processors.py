from django.middleware.csrf import get_token
from blog.models import Article


def breadcrumbs_urls(request):
    arr = request.path.split(sep='/')[1:]
    titles = [title.replace('-', ' ').title() for title in arr]
    paths = []

    for parent_index, parent_loop in enumerate(arr):
        path = ''

        for child_index, child_loop in enumerate(arr):
            if child_index <= parent_index:
                path += '/' + child_loop

        paths.append(path)

    titles = titles[:-1]
    paths = paths[:-1]

    return {
        'urls': list(zip(titles, paths))
    }


def generate_token(request):
    return {
        'csrf_token': get_token(request=request)
    }


def latest_articles(request):
    return {
        'latest_articles': Article.objects.all().order_by('-date_posted')[:3]
    }
