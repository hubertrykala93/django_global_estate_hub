from .models import Category, Article


def get_category_info(request, category):
    return {
        'get_category_info': Article.objects.filter(category=category)
    }
    # return {
    #     'get_category_info': list(
    #         zip(
    #             [category.slug for category in Category.objects.all()],
    #             [category.get_absolute_url() for category in Category.objects.all()],
    #             [category.name for category in Category.objects.all()],
    #             [Article.objects.filter(category=category).count() for category in Category.objects.all()]
    #         )
    #     ),
    # }


def newest_articles(request):
    return {
        'newest_articles': Article.objects.order_by('-date_posted')[:4],
    }


def categories(request):
    return {
        'categories': Category.objects.all(),
    }
