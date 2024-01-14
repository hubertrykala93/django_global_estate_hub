from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Newsletter, ContactMail
import json
import re
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os
from dotenv import load_dotenv
from django.utils.html import strip_tags
from properties.models import Property, City

load_dotenv()


def index(request):
    """
    Returns an HttpResponse with the homepage template.

    return: HttpResponse
    """
    return render(request=request, template_name='core/index.html', context={
        'title': 'Home',
    })


def newsletter(request):
    """
    The function handling the form for saving an email address for the newsletter to the database
    using the POST method with Asynchronous JavaScript and XMLHttpRequest (AJAX) request.
    Upon successful form validation, an email message is automatically sent
    from the website administrator to the provided email address.

    return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        email, spam_verification = [data[key] for key in data.keys()]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
                "message": "",
            })

        response = {
            "valid":
                False if not email else
                False if not re.match(pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                      string=email) else
                False if re.match(pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                  string=email) and Newsletter.objects.filter(email=email).exists() else
                True,
            "message":
                "The email field cannot be empty." if not email else
                "The e-mail address format is invalid." if not re.match(
                    pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', string=email) else
                f"The e-mail address {email} already exists." if re.match(
                    pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                    string=email) and Newsletter.objects.filter(
                    email=email).exists() else
                "Congratulations! You have successfully subscribed to our newsletter.",
        }

        if response['valid']:
            new_subscriber = Newsletter(email=email)
            new_subscriber.save()

            try:
                html_message = render_to_string(template_name='core/newsletter_mail.html', context={
                    'email': email,
                })
                plain_message = strip_tags(html_message)

                message = EmailMultiAlternatives(
                    subject='Thank you for subscribing to our newsletter!',
                    body=plain_message,
                    from_email=os.environ.get("EMAIL_HOST_USER"),
                    to=[email],
                )

                message.attach_alternative(content=html_message, mimetype='text/html')
                message.send(fail_silently=True)

                return JsonResponse(data=response)

            except Exception:
                return JsonResponse(data={
                    "valid": False,
                    "message": "Unfortunately, we were unable to sign up your email for our newsletter. "
                               "Please try again.",
                })

        else:
            return JsonResponse(data=response)


def about(request):
    """
    Returns an HttpResponse with the about template.

    return: HttpResponse
    """
    return render(request=request, template_name='core/about.html', context={
        'title': 'About',
    })


def faq(request):
    """
    Returns an HttpResponse with the FAQ template.

    return: HttpResponse
    """
    return render(request=request, template_name='core/faq.html', context={
        'title': 'Faq',
    })


def contact(request):
    """
    Returns an HttpResponse with the contact template.

    return: HttpResponse
    """
    return render(request=request, template_name='core/contact.html', context={
        'title': 'Contact',
    })


def error(request):
    """
    Returns an HttpResponse with the error404 template.

    return: HttpResponse
    """
    return render(request=request, template_name='core/error.html', context={
        'title': 'Error 404',
    })


def send_message(request):
    """
    The function handling the form for sending an email message to the website administrator
    using the POST method with Asynchronous JavaScript and XMLHttpRequest (AJAX) request.
    The function also saves data such as Full Name, Phone Number, Email Address, and Message to the database.
    Upon successful form validation, an email message is automatically sent to the website administrator.

    return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        fullname, phone_number, email, content = [data[key][0] for key in list(data.keys())[:-1]]
        spam_verification = [data[key] for key in data][-1]
        fullname_field, phone_field, email_field, content_field = [data[key][1] for key in list(data.keys())[:-1]]
        fullname_label, phone_label, email_label, content_label = [data[key][2] for key in list(data.keys())[:-1]]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
            }, safe=False)

        response = [
            {
                "valid":
                    False if not fullname else
                    True,
                "field": fullname_field,
                "message":
                    f"The {fullname_label} field cannot be empty." if not fullname else
                    "",
            },
            {
                "valid":
                    False if not phone_number else
                    False if not re.match(pattern="^\\+?[1-9][0-9]{7,14}$",
                                          string=phone_number) else
                    True,
                "field": phone_field,
                "message":
                    f"The {phone_label} field cannot be empty." if not phone_number else
                    f"The {phone_label} format is invalid." if not re.match(
                        pattern="^\\+?[1-9][0-9]{7,14}$",
                        string=phone_number) else
                    "",
            },
            {
                "valid":
                    False if not email else
                    False if not re.match(pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                          string=email) else
                    True,
                "field": email_field,
                "message":
                    f"The {email_label} field cannot be empty." if not email else
                    f"The {email_label} format is invalid." if not re.match(
                        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', string=email) else
                    "",
            },
            {
                "valid":
                    False if not content else
                    True,
                "field": content_field,
                "message":
                    f"The {content_label} field cannot be empty." if not content else
                    "",
            }
        ]

        validation = list(set([data['valid'] for data in response]))

        if len(validation) == 1:
            if validation[0]:
                new_mail = ContactMail(full_name=fullname, phone_number=phone_number, email=email, content=content)
                new_mail.save()

                try:
                    html_message = render_to_string(template_name='core/contact_mail.html', context={
                        'fullname': fullname,
                        'phone_number': phone_number,
                        'email': email,
                        'content': content,
                    })
                    plain_message = strip_tags(html_message)

                    message = EmailMultiAlternatives(
                        subject=f"E-mail from Global Estate Hub.",
                        body=plain_message,
                        from_email=os.environ.get("EMAIL_HOST_USER"),
                        to=[os.environ.get("EMAIL_HOST_USER")],
                        headers={'Reply-To': email},
                    )

                    message.attach_alternative(content=html_message, mimetype='text/html')
                    message.send(fail_silently=True)

                    return JsonResponse(data=response, safe=False)

                except Exception:
                    return JsonResponse(data={
                        "valid": False,
                        "message": "The message could not be sent."
                    }, safe=False)

            else:
                return JsonResponse(data=response, safe=False)

        else:
            return JsonResponse(data=response, safe=False)
