import django.core.paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category, Tag, Comment, CommentLike, CommentDislike
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from accounts.models import User


def blog_pagination(request, object_list, per_page) -> django.core.paginator.Page:
    """
    Returns Page object for pagination.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        object_list: django.db.models.query.Queryset
        per_page: int

    Returns
    ----------
        django.core.paginator.Page
    """
    paginator = Paginator(object_list=object_list, per_page=per_page)
    page = request.GET.get('page')

    pages = paginator.get_page(number=page)

    if page is None:
        pages = paginator.get_page(number=1)

    else:
        if page not in list(str(i) for i in pages.paginator.page_range):
            return redirect(to='error')

    return pages


def blog(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the blog template along with pagination.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    return render(request=request, template_name='blog/blog.html', context={
        'title': 'Blog',
        'pages': blog_pagination(request=request, object_list=Article.objects.order_by('-date_posted'), per_page=8),
    })


def article_categories(request, category_slug) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the article categories template along with pagination.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        category_slug: str

    Returns
    ----------
        django.http.response.HttpResponse
    """
    category = get_object_or_404(klass=Category, slug=category_slug)

    return render(request=request, template_name='blog/article-categories.html', context={
        'title': category,
        'category': category,
        'pages': blog_pagination(request=request,
                                 object_list=Article.objects.filter(category=category).order_by('-date_posted'),
                                 per_page=8),
    })


def article_tags(request, tag_slug) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the article tags template along with pagination.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        tag_slug: str

    Returns
    ----------
        django.http.response.HttpResponse
    """
    tag = get_object_or_404(klass=Tag, slug=tag_slug)

    return render(request=request, template_name='blog/article-tags.html', context={
        'title': tag,
        'pages': blog_pagination(request=request, object_list=Article.objects.filter(tags=tag).order_by('-date_posted'),
                                 per_page=8),
    })


def article_details(request, category_slug, article_slug) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the article-details template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        category_slug: str
        article_slug: str

    Returns
    ----------
        django.http.response.HttpResponse
    """
    category = Category.objects.get(slug=category_slug)
    article = Article.objects.get(slug=article_slug)
    comments = Comment.objects.filter(article=article, active=True)
    comments_counter = len(comments) - len(
        [obj.parent for obj in Comment.objects.filter(article=article, active=True) if obj.parent is not None])
    next_article = Article.objects.filter(date_posted__gt=article.date_posted).order_by('date_posted').first()
    previous_article = Article.objects.filter(date_posted__lt=article.date_posted).order_by('-date_posted').first()
    user_likes = [obj.comment for obj in CommentLike.objects.filter(user=request.user.id)]
    user_dislikes = [obj.comment for obj in CommentDislike.objects.filter(user=request.user.id)]

    return render(request=request, template_name='blog/article-details.html', context={
        'title': article.title,
        'category': category,
        'article': article,
        'comments': comments,
        'comments_counter': comments_counter,
        'article_tags': article.tags.all(),
        'previous_article': previous_article,
        'next_article': next_article,
        'user_likes': user_likes,
        'user_dislikes': user_dislikes,
    })


def blog_results(request) -> django.http.response.HttpResponse or django.http.response.HttpResponseRedirect:
    """
    Returns an HttpResponse with the blog-results template along with pagination.

    On this page, articles are listed based on keywords provided by the user
    and retrieved through the GET request method. Model attributes such as title and content are searched.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse or django.http.response.HttpResponseRedirect
    """
    articles = []

    if 'search' in request.GET:
        if request.GET.get('search'):
            keywords = request.GET.get('search').split()

            for keyword in keywords:
                articles.extend(Article.objects.filter(title__icontains=keyword).order_by('date_posted'))
                articles.extend(Article.objects.filter(content__icontains=keyword).order_by('-date_posted'))

            return render(request=request, template_name='blog/blog-results.html', context={
                'title': 'Blog Results',
                'articles': articles,
                'pages': blog_pagination(request=request, object_list=articles, per_page=8),
            })

        else:
            return redirect(to='blog')

    else:
        return redirect(to='blog')


def add_comment(request, category_slug, article_slug) -> django.http.response.JsonResponse:
    """
    The function handles the comment submission form for a specific article by both logged-in and non-logged-in users.
    If the comment is added by a non-logged-in user, they can enter their own name in the 'Name' field.
    However, if the comment is added by a logged-in user, their username is automatically assigned.
    The function utilizes the PATCH method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the data is saved in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        category_slug: str
        article_slug: str

    Returns
    ----------
        django.http.response.JsonResponse
    """
    category = Category.objects.get(slug=category_slug)
    article = get_object_or_404(klass=Article, slug=article_slug, category=category)

    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        full_name, comment = [data[key] for key in data][0][0], [data[key] for key in data][1][0]
        full_name_field, comment_field = [data[key] for key in data][0][1], [data[key] for key in data][1][1]
        full_name_label, comment_label = [data[key] for key in data][0][2], [data[key] for key in data][1][2]
        spam_verification = [data[key] for key in data][-1]

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
            if request.user.is_anonymous:
                user = User()
                user.save()

                comment = Comment(user=user, article=article, full_name=full_name, comment=comment)
                comment.save()

                user.delete()

            else:
                user = User.objects.get(username=request.user)
                comment = Comment(user=user, article=article, comment=comment)
                comment.save()

            return JsonResponse(data={
                "valid": True,
                "message": "The comment has been submitted for approval by the administrator.",
            }, safe=False)
        else:
            return JsonResponse(data=response, safe=False)


def edit_comment(request, category_slug, article_slug) -> django.http.response.JsonResponse:
    """
    The function handles the comment editing form for a specific article by a logged-in user.
    The function utilizes the PATCH method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the data is updated in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        category_slug: str
        article_slug: str

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'PATCH':
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


def delete_comment(request, category_slug, article_slug) -> django.http.response.JsonResponse:
    """
    The function handles the comment deletion form for a specific article by a logged-in user.
    The function utilizes the DELETE method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the data is updated in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        category_slug: str
        article_slug: str

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'DELETE':
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

            category = Category.objects.get(slug=category_slug)
            article = Article.objects.get(category=category, slug=article_slug)
            comments_counter = len(Comment.objects.filter(article=article, active=True)) - len(
                [obj.parent for obj in Comment.objects.filter(article=article, active=True) if obj.parent is not None])

            response.update({
                "commentsCounter": comments_counter
            })

            return JsonResponse(data=response)

        else:
            return JsonResponse(data=response)


def give_like(request, category_slug, article_slug) -> django.http.response.JsonResponse:
    """
    The function handles the like submission form for the current comment in a given article.
    If the user has already liked the comment, the like is removed,
    and the number of likes in the 'Comment' model is updated by -1. However,
    if the user had previously disliked the comment and then liked it,
    the number of dislikes in the 'Comment' model is updated.
    The function utilizes the POST method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the data is updated in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        category_slug: str
        article_slug: str

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'PUT':
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


def give_dislike(request, category_slug, article_slug) -> django.http.response.JsonResponse:
    """
    The function handles the form for adding a dislike to the current comment in a given article.
    If the comment has already been disliked by the user, the dislike is removed,
    and the number of dislikes in the 'Comment' model is updated by -1. However,
    if the user previously liked the comment and then gave it a dislike,
    the number of likes in the 'Comment' model is updated.
    The function uses the POST method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the data is updated in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        category_slug: str
        article_slug: str

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'PUT':
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


def reply_comment(request, category_slug, article_slug) -> django.http.response.JsonResponse:
    """
    The function handles the form for adding a reply to a comment in a given article
    by both logged-in and non-logged-in users. If the reply is added by a non-logged-in user,
    they can enter their own name in the 'Name' field. However, if the reply is added by a logged-in user,
    their username is automatically assigned.
    The function uses the POST method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the data is saved in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        category_slug: str
        article_slug: str

    Returns
    ----------
        django.http.response.JsonResponse
    """
    category = Category.objects.get(slug=category_slug)
    article = get_object_or_404(klass=Article, slug=article_slug, category=category)

    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        comment_id = int([data[key] for key in data.keys()][0])
        full_name, full_name_field, full_name_label = [data[key] for key in data.keys()][1]
        comment, comment_field, comment_label = [data[key] for key in data.keys()][2]
        spam_verification = [data[key] for key in data.keys()][3]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
            }, safe=False)

        if request.user.is_anonymous:
            response = [
                {
                    "valid":
                        False if not full_name else
                        False if User.objects.filter(username=full_name).exists() else
                        True,
                    "field": full_name_field,
                    "message":
                        f"The {full_name_label} field cannot be empty." if not full_name else
                        f"The name {full_name} is already taken. Please choose another one." if User.objects.filter(
                            username=full_name).exists() else
                        "",
                },
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

        else:
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

        validation = list(set([data['valid'] for data in response]))

        if all(validation):
            if request.user.is_anonymous:
                user = User()
                user.save()

                parent = Comment.objects.get(pk=comment_id)
                reply = Comment(user=user, full_name=full_name, article=article, comment=comment, parent=parent)
                reply.save()

                user.delete()

            else:
                user = User.objects.get(username=request.user)
                parent = Comment.objects.get(pk=comment_id)
                reply = Comment(user=user, article=article, comment=comment, parent=parent)
                reply.save()

            return JsonResponse(data={
                "valid": True,
                "message": "The comment has been submitted for approval by the administrator.",
            }, safe=False)

        else:
            return JsonResponse(data=response, safe=False)
