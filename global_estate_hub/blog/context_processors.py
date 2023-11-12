from .models import Category, Tag


def categories(request):
    return {
        'categories': Category.objects.all(),
    }


def tags(request):
    return {
        'tags': Tag.objects.all()
    }
