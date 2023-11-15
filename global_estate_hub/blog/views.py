from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.core.paginator import Paginator


def blog(request):
    paginator = Paginator(object_list=Article.objects.order_by('-date_posted'), per_page=9)
    page = request.GET.get('page')

    if page is None:
        pages = paginator.get_page(number=page)

    elif page == '0':
        pages = paginator.get_page(number=1)

    elif paginator.num_pages >= int(page) >= 1:
        pages = paginator.get_page(number=page)

    else:
        return render(request=request, template_name='core/error.html', context={
            'title': 'Error 404',
        })

    return render(request=request, template_name='blog/blog.html', context={
        'title': 'Blog',
        'pages': pages,
    })


def article_categories(request, category_slug):
    category = get_object_or_404(klass=Category, slug=category_slug)

    paginator = Paginator(object_list=Article.objects.filter(category=category).order_by('date_posted'), per_page=9)
    page = request.GET.get('page')

    if page is None:
        pages = paginator.get_page(number=page)

    elif page == '0':
        pages = paginator.get_page(number=1)

    elif paginator.num_pages >= int(page) >= 1:
        pages = paginator.get_page(number=page)

    else:
        return render(request=request, template_name='core/error.html', context={
            'title': 'Error 404',
        })

    return render(request=request, template_name='blog/article-categories.html', context={
        'title': category,
        'category': category,
        'pages': pages,
    })


def article_details(request, category_slug, article_slug):
    category = get_object_or_404(klass=Category, slug=category_slug)
    article = get_object_or_404(klass=Article, category=category, slug=article_slug)

    return render(request=request, template_name='blog/article-details.html', context={
        'title': article.title,
        'category': category,
        'article': article,
    })
