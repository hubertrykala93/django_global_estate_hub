from .models import Category, Article, Tag
from accounts.models import User


def get_category_info(request) -> dict:
    """
    Returns full information about categories.

    return dict
    """
    return {
        'get_category_info': list(
            zip(
                [category.slug for category in Category.objects.all()],
                [category.get_absolute_url() for category in Category.objects.all()],
                [category.name for category in Category.objects.all()],
                [Article.objects.filter(category=category).count() for category in Category.objects.all()]
            )
        ),
    }


def newest_articles(request) -> dict:
    """
    Creates a query set for the database and returns the four most recent articles from the Blog application,
    which are then rendered in the Blog sidebar.

    return: dict
    """
    return {
        'newest_articles': Article.objects.order_by('-date_posted')[:4],
    }


def popular_tags(request):
    """
    Returns a set of queries with the most frequently occurring tags.

    return: dict
    """
    articles = Article.objects.all()

    result = []

    for article in articles:
        for obj in article.tags.all():
            result.append(obj.name)

    tags_dict = {}

    for tag in result:
        if tag not in tags_dict.keys():
            tags_dict[tag] = 1
        else:
            tags_dict[tag] += 1

    return {
        'popular_tags': Tag.objects.filter(
            name__in=list(dict(sorted(tags_dict.items(), key=lambda x: x[1], reverse=True)).keys())[:6])
    }


def users(request):
    """
    Creates a set of queries to the database and returns all registered users in the database.

    return: dict
    """
    return {
        'users': User.objects.all()
    }
