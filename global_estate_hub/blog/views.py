from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage


def blog(request):
    paginator = Paginator(object_list=Article.objects.all(), per_page=3)
    page = request.GET.get('page')

    try:
        articles = paginator.get_page(number=page)

    except PageNotAnInteger:
        page = 1
        articles = paginator.page(number=page)

    except EmptyPage:
        page = paginator.num_pages
        articles = paginator.page(number=page)

    return render(request=request, template_name='blog/blog.html', context={
        'title': 'Blog',
        'pages': articles,
        'paginator': paginator,
    })


def article_categories(request, category_slug):
    category = get_object_or_404(klass=Category, slug=category_slug)
    articles = Article.objects.filter(category=category)

    return render(request=request, template_name='blog/article-categories.html', context={
        'title': category,
        'category': category,
        'articles': articles,
    })


def article_details(request, category_slug, article_slug):
    category = get_object_or_404(klass=Category, slug=category_slug)
    article = get_object_or_404(klass=Article, category=category, slug=article_slug)

    return render(request=request, template_name='blog/article-details.html', context={
        'title': article.title,
        'category': category,
        'article': article,
    })
