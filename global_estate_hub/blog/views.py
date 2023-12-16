from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category, Tag
from django.core.paginator import Paginator


def blog(request):
    """
    Returns an HttpResponse with the blog template along with pagination.

    return: HttpResponse
    """
    paginator = Paginator(object_list=Article.objects.order_by('-date_posted'), per_page=8)
    page = request.GET.get('page')

    pages = paginator.get_page(number=page)

    if page is None:
        pages = paginator.get_page(number=1)

    else:
        if page not in list(str(i) for i in pages.paginator.page_range):
            return redirect(to='error')

    return render(request=request, template_name='blog/blog.html', context={
        'title': 'Blog',
        'pages': pages,
    })


def article_categories(request, category_slug):
    """
    Returns an HttpResponse with the article categories template along with pagination.

    return: HttpResponse
    """
    category = get_object_or_404(klass=Category, slug=category_slug)

    paginator = Paginator(object_list=Article.objects.filter(category=category).order_by('date_posted'), per_page=8)
    page = request.GET.get('page')

    pages = paginator.get_page(number=page)

    if page is None:
        pages = paginator.get_page(number=1)

    else:
        if page not in list(str(i) for i in pages.paginator.page_range):
            return redirect(to='error')

    return render(request=request, template_name='blog/article-categories.html', context={
        'title': category,
        'category': category,
        'pages': pages,
    })


def article_tags(request, tag_slug):
    """
    Returns an HttpResponse with the article tags template along with pagination.

    return: HttpResponse
    """
    tag = get_object_or_404(klass=Tag, slug=tag_slug)

    paginator = Paginator(object_list=Article.objects.filter(tags=tag).order_by('date_posted'), per_page=8)
    page = request.GET.get('page')

    pages = paginator.get_page(number=page)

    if page is None:
        pages = paginator.get_page(number=1)

    else:
        if page not in list(str(i) for i in pages.paginator.page_range):
            return redirect(to='error')

    return render(request=request, template_name='blog/article-categories.html', context={
        'title': tag,
        'pages': pages,
    })


def article_details(request, category_slug, article_slug):
    """
    Returns an HttpResponse with the article-details template.

    return: HttpResponse
    """

    category = Category.objects.get(slug=category_slug)
    article = Article.objects.get(slug=article_slug)

    next_article = Article.objects.filter(date_posted__gt=article.date_posted).order_by('date_posted').first()
    previous_article = Article.objects.filter(date_posted__lt=article.date_posted).order_by('-date_posted').first()

    return render(request=request, template_name='blog/article-details.html', context={
        'title': article.title,
        'category': category,
        'article': article,
        'article_tags': article.tags.all(),
        'previous_article': previous_article,
        'next_article': next_article,
    })


def blog_results(request):
    """
    Returns an HttpResponse with the blog-results template along with pagination.

    On this page, articles are listed based on keywords provided by the user
    and retrieved through the GET request method. Model attributes such as title and content are searched.

    return: HttpResponse
    """
    if 'search' in request.GET:
        if request.GET.get('search'):
            keywords = request.GET.get('search').split()

            articles = []

            for keyword in keywords:
                articles.extend(
                    Article.objects.filter(title__icontains=keyword).order_by('date_posted') and
                    Article.objects.filter(content__icontains=keyword).order_by('-date_posted')
                )

            paginator = Paginator(object_list=articles, per_page=8)
            page = request.GET.get('page')

            pages = paginator.get_page(number=page)

            if page is None:
                pages = paginator.get_page(number=1)

            else:
                if page not in list(str(i) for i in pages.paginator.page_range):
                    return redirect(to='error')

            return render(request=request, template_name='blog/blog-results.html', context={
                'title': 'Blog Results',
                'pages': pages,
            })

        else:
            articles = Article.objects.all().order_by('-date_posted')

            paginator = Paginator(object_list=articles, per_page=8)
            page = request.GET.get('page')

            pages = paginator.get_page(number=page)

            if page is None:
                pages = paginator.get_page(number=1)

            else:
                if page not in list(str(i) for i in pages.paginator.page_range):
                    return redirect(to='error')

            return render(request=request, template_name='blog/blog-results.html', context={
                'title': 'Blog Results',
                'pages': pages,
            })

    else:
        return render(request=request, template_name='blog/blog-results.html', context={
            'title': 'Blog Results',
        })
