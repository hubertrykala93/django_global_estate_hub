from django.shortcuts import render
from django.http import JsonResponse
from .models import Newsletter
import json
import re
from django.core.mail import BadHeaderError, EmailMessage
from django.template.loader import render_to_string
import os
from dotenv import load_dotenv

load_dotenv()


def index(request):
    return render(request=request, template_name='core/index.html', context={
        'title': 'Home',
    })


def newsletter(request):
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))
        email = data['email']
        spam_verification = data['url']
        # spam_verification = spam_verification + '123'

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": -1,
                "message": "",
            })

        response = {
            "valid":
                0 if not email else
                0 if not re.match(pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$', string=email) else
                0 if re.match(pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$',
                              string=email) and Newsletter.objects.filter(email=email).exists() else
                1,
            "message":
                "The email field cannot be empty." if not email else
                "The e-mail address format is invalid." if not re.match(
                    pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$', string=email) else
                f"The e-mail address {email} already exists." if re.match(
                    pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$',
                    string=email) and Newsletter.objects.filter(
                    email=email).exists() else
                "Congratulations! You have successfully subscribed to our newsletter.",
        }

        if response['valid'] == 1:
            new_subscriber = Newsletter(email=email)
            new_subscriber.save()

            try:
                message = EmailMessage(
                    subject='Thank you for subscribing to our newsletter!',
                    body=render_to_string(template_name='core/newsletter_mail.html', context={
                        "email": email,
                    }),
                    from_email=os.environ.get("EMAIL_HOST_USER"),
                    to=[email],
                )

                message.send(fail_silently=True)

                return JsonResponse(data=response)

            except BadHeaderError:
                return JsonResponse(data={
                    "valid": 0,
                    "message": "Unfortunately, we were unable to sign up your email for our newsletter. "
                               "Please try again.",
                })

        else:
            return JsonResponse(data=response)


def about(request):
    return render(request=request, template_name='core/about.html', context={
        'title': 'About',
    })


def properties(request):
    return render(request=request, template_name='core/properties.html', context={
        'title': 'Properties',
    })


def faq(request):
    return render(request=request, template_name='core/faq.html', context={
        'title': 'Faq',
    })


def contact(request):
    return render(request=request, template_name='core/contact.html', context={
        'title': 'Contact',
    })


def error(request):
    return render(request=request, template_name='core/error.html', context={
        'title': 'Error 404',
    })
