from .models import Category, Article, Tag
from accounts.models import User


def get_category_info(request) -> dict:
    """
    Returns full information about categories.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    return {
        "get_category_info": list(
            zip(
                [category.slug for category in Category.objects.all()],
                [category.get_absolute_url() for category in Category.objects.all()],
                [category.name for category in Category.objects.all()],
                [
                    Article.objects.filter(category=category).count()
                    for category in Category.objects.all()
                ],
            )
        ),
    }


def newest_articles(request) -> dict:
    """
    Creates a query set for the database and returns the four most recent articles from the Blog application,
    which are then rendered in the Blog sidebar.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    return {
        "newest_articles": Article.objects.order_by("-date_posted")[:4],
    }


def popular_tags(request) -> dict:
    """
    Returns a set of queries with the most frequently occurring tags.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    all_tags = [
        obj.name for article in Article.objects.all() for obj in article.tags.all()
    ]
    tags_dict = {tag: all_tags.count(tag) for tag in set(all_tags)}

    return {
        "popular_tags": Tag.objects.filter(
            name__in=list(
                dict(sorted(tags_dict.items(), key=lambda x: x[1], reverse=True)).keys()
            )[:6]
        )
    }


def users(request) -> dict:
    """
    Creates a set of queries to the database and returns all registered users in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        dict
    """
    return {"users": User.objects.all()}
