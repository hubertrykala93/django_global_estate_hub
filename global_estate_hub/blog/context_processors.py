from .models import Category, Tag, Article


def articles(request):
    return {
        'articles': Article.objects.all()
    }


def categories(request):
    return {
        'categories': Category.objects.all(),
    }


def tags(request):
    return {
        'tags': Tag.objects.all()
    }
