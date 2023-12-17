from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category, Tag, Comment
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
import uuid
from accounts.models import User


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
    comments = Comment.objects.filter(article=article)

    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(s=request.body.decode('utf-8'))

            _, comment = [data[key][0] for key in list(data.keys())[:-1]]
            spam_verification = [data[key] for key in data][-1]
            _, comment_field = [data[key][1] for key in list(data.keys())[:-1]]
            _, comment_label = [data[key][2] for key in list(data.keys())[:-1]]

            if len(spam_verification) != 0:
                return JsonResponse(data={
                    "valid": None,
                }, safe=False)

            response = [
                {
                    "valid":
                        False if not comment else
                        True,
                    "field": comment_field,
                    "message":
                        f"The {comment_label} field cannot be empty." if not comment else
                        "",
                }
            ]

            validation = [data['valid'] for data in response]

            if all(validation):
                comment = Comment(user_id=request.user.id, article=article,
                                  comment=comment)
                comment.save()

                return JsonResponse(data={
                    "valid": True,
                    "message": "The comment has been submitted for approval by the administrator.",
                }, safe=False)
            else:
                return JsonResponse(data=response, safe=False)

        elif request.user.is_anonymous:
            data = json.loads(s=request.body.decode('utf-8'))

            full_name, comment = [data[key][0] for key in list(data.keys())[:-1]]
            spam_verification = [data[key] for key in data][-1]
            full_name_field, comment_field = [data[key][1] for key in list(data.keys())[:-1]]
            full_name_label, comment_label = [data[key][2] for key in list(data.keys())[:-1]]

            if len(spam_verification) != 0:
                return JsonResponse(data={
                    "valid": None,
                }, safe=False)

            response = [
                {
                    "valid":
                        False if not full_name else
                        True,
                    "field": full_name_field,
                    "message":
                        f"The {full_name_label} field cannot be empty." if not full_name else
                        "",
                },
                {
                    "valid":
                        False if not comment else
                        True,
                    "field": comment_field,
                    "message":
                        f"The {comment_label} field cannot be empty." if not full_name else
                        "",
                }
            ]

            validation = list(set([data['valid'] for data in response]))

            if all(validation):
                user = User()
                user.save()

                comment = Comment(user=user, article=article, full_name=full_name, comment=comment)
                comment.save()

                user.delete()

                return JsonResponse(data={
                    "valid": True,
                    "message": "The comment has been submitted for approval by the administrator.",
                }, safe=False)

            else:
                return JsonResponse(data=response, safe=False)

    else:

        next_article = Article.objects.filter(date_posted__gt=article.date_posted).order_by('date_posted').first()
        previous_article = Article.objects.filter(date_posted__lt=article.date_posted).order_by('-date_posted').first()

        return render(request=request, template_name='blog/article-details.html', context={
            'title': article.title,
            'category': category,
            'article': article,
            'comments': comments,
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
