from django.middleware.csrf import get_token
from blog.models import Article


def breadcrumbs_urls(request) -> dict:
    """
    Creating breadcrumbs for the entire project.

    return: dict
    """
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


def generate_token(request) -> dict:
    """
    Generating CSRF middleware tokens for all forms in the project.

    return: dict
    """
    return {
        'csrf_token': get_token(request=request)
    }


def latest_articles(request) -> dict:
    """
    Creates a query set for the database and returns the three most recent articles from the Blog application,
    which are then rendered in the Blog section on the homepage.

    return: dict
    """
    return {
        'latest_articles': Article.objects.all().order_by('-date_posted')[:3]
    }
