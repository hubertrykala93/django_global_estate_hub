from django.shortcuts import render, get_object_or_404
from .models import Article, Category


def blog(request):
    articles = Article.objects.all()

    return render(request=request, template_name='blog/blog.html', context={
        'title': 'Blog',
        'articles': articles,
    })


def article_categories(request, category_slug):
    category = get_object_or_404(klass=Category, slug=category_slug)
    articles = Article.objects.filter(category=category)

    return render(request=request, template_name='blog/article_categories.html', context={
        'title': category,
        'category': category,
        'articles': articles,
    })


def article_details(request, category_slug, article_slug):
    category = get_object_or_404(klass=Category, slug=category_slug)
    article = get_object_or_404(klass=Article, slug=article_slug)

    return render(request=request, template_name='blog/article-details.html', context={
        'title': article.title,
        'category': category,
        'article': article,
    })
