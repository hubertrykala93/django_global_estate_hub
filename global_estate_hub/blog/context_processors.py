from .models import Category, Article
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def length_categories(request):
    categories = Category.objects.all()

    category_slugs = []
    category_urls = []
    category_titles = []
    category_lengths = []

    for category in categories:
        category_slugs.append(category.slug)
        category_urls.append(category.get_absolute_url())
        category_titles.append(category.name)
        category_lengths.append(Article.objects.filter(category=category).count())

    return {
        'category_length': list(zip(category_slugs, category_urls, category_titles, category_lengths)),
    }


def newest_articles(request):
    return {
        'newest_articles': Article.objects.order_by('-date_posted')[:4],
    }


def categories(request):
    return {
        'categories': Category.objects.all(),
    }
