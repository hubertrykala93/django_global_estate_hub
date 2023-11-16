from .models import Category, Article


def length_categories(request):
    categories = Category.objects.all()

    category_slugs = [category.slug for category in categories]
    category_urls = [category.get_absolute_url() for category in categories]
    category_titles = [category.name for category in categories]
    category_lengths = [Article.objects.filter(category=category).count() for category in categories]

    return {
        'category_length': list(
            zip(
                category_slugs,
                category_urls,
                category_titles,
                category_lengths
            )
        ),
    }


def newest_articles(request):
    return {
        'newest_articles': Article.objects.order_by('-date_posted')[:4],
    }


def categories(request):
    return {
        'categories': Category.objects.all(),
    }
