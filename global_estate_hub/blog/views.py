from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category, Tag, Comment, CommentLike, CommentDislike
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    comments = Comment.objects.filter(article=article, active=True)
    next_article = Article.objects.filter(date_posted__gt=article.date_posted).order_by('date_posted').first()
    previous_article = Article.objects.filter(date_posted__lt=article.date_posted).order_by('-date_posted').first()
    user_likes = [obj.comment for obj in CommentLike.objects.filter(user=request.user.id)]
    user_dislikes = [obj.comment for obj in CommentDislike.objects.filter(user=request.user.id)]

    return render(request=request, template_name='blog/article-details.html', context={
        'title': article.title,
        'category': category,
        'article': article,
        'comments': comments,
        'article_tags': article.tags.all(),
        'previous_article': previous_article,
        'next_article': next_article,
        'user_likes': user_likes,
        'user_dislikes': user_dislikes,
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


def add_comment(request, category_slug, article_slug):
    category = Category.objects.get(slug=category_slug)
    article = get_object_or_404(klass=Article, slug=article_slug, category=category)

    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(s=request.body.decode('utf-8'))

            comment = [data[key] for key in list(data.keys())][1][0]
            spam_verification = [data[key] for key in data][-1]
            comment_field = [data[key] for key in list(data.keys())][1][1]
            comment_label = [data[key] for key in list(data.keys())][1][2]

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
                user = User.objects.get(username=request.user)
                comment = Comment(user=user, article=article,
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
                        False if User.objects.filter(username=full_name) else
                        True,
                    "field": full_name_field,
                    "message":
                        f"The {full_name_label} field cannot be empty." if not full_name else
                        f"The name {full_name} is already taken. Please choose another one."
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


@csrf_exempt
def edit_comment(request, category_slug, article_slug):
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        comment_id = data['commentId']
        comment_content = [data[key] for key in list(data.keys())][1][0]

        response = {
            "valid":
                False if not comment_content else
                False if comment_content == Comment.objects.get(id=comment_id).comment else
                True,
            "commentId": comment_id,
            "newContent": comment_content,
            "message":
                "You cannot add an empty comment." if not comment_content else
                "The comment was not edited correctly because its content did not change." if comment_content == Comment.objects.get(
                    id=comment_id).comment else
                "",
        }

        if response['valid']:
            comment = Comment.objects.get(id=comment_id)

            comment.comment = comment_content
            comment.save()

            return JsonResponse(data=response)

        else:
            return JsonResponse(data=response)


@csrf_exempt
def delete_comment(request, category_slug, article_slug):
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        comment_id = data['commentId']

        response = {
            "valid":
                False if not Comment.objects.filter(id=comment_id).exists() else
                True,
            "commentId": comment_id,
            "message":
                "The comment does not exist." if not Comment.objects.filter(id=comment_id).exists() else
                "Your comment has been deleted.",
        }

        if response['valid']:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()

            return JsonResponse(data=response)

        else:
            return JsonResponse(data=response)


@csrf_exempt
def give_like(request, category_slug, article_slug):
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))
        comment_id = int(data['commentId'])

        comment = Comment.objects.get(id=comment_id)

        user = User.objects.get(username=request.user)

        like = CommentLike(user=user, comment=comment)

        if CommentDislike.objects.filter(user=user, comment=comment).exists():
            CommentDislike.objects.filter(user=user, comment=comment).delete()

            comment.dislikes -= 1
            comment.save()

        if CommentLike.objects.filter(user=user, comment=comment).exists():
            CommentLike.objects.filter(user=user, comment=comment).delete()
            comment.likes -= 1
            comment.save()

            return JsonResponse(data={
                "valid": False,
                "commentId": comment_id,
                "likes": comment.likes,
                "dislikes": comment.dislikes,
            })

        else:
            like.save()

            comment.likes += 1
            comment.save()

            return JsonResponse(data={
                "valid": True,
                "commentId": comment_id,
                "likes": comment.likes,
                "dislikes": comment.dislikes,
            })


@csrf_exempt
def give_dislike(request, category_slug, article_slug):
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))
        comment_id = int(data['commentId'])

        comment = Comment.objects.get(id=comment_id)
        user = User.objects.get(username=request.user)

        dislike = CommentDislike(user=user, comment=comment)

        if CommentLike.objects.filter(user=user, comment=comment).exists():
            CommentLike.objects.filter(user=user, comment=comment).delete()

            comment.likes -= 1
            comment.save()

        if CommentDislike.objects.filter(user=user, comment=comment).exists():
            CommentDislike.objects.filter(user=user, comment=comment).delete()
            comment.dislikes -= 1
            comment.save()

            return JsonResponse(data={
                "valid": False,
                "commentId": comment_id,
                "likes": comment.likes,
                "dislikes": comment.dislikes,
            })

        else:
            dislike.save()

            comment.dislikes += 1
            comment.save()

            return JsonResponse(data={
                "valid": True,
                "commentId": comment_id,
                "likes": comment.likes,
                "dislikes": comment.dislikes,
            })
