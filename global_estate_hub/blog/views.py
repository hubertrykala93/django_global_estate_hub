from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category
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
    Returns an HttpResponse with the article-categories template along with pagination.

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


def article_details(request, category_slug, article_slug):
    """
    Returns an HttpResponse with the article-details template.

    return: HttpResponse
    """
    category = get_object_or_404(klass=Category, slug=category_slug)
    article = get_object_or_404(klass=Article, category=category, slug=article_slug)

    return render(request=request, template_name='blog/article-details.html', context={
        'title': article.title,
        'category': category,
        'article': article,
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
