import os
import django.http.response
from django.shortcuts import render, redirect, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from .models import User, Individual, Business
import json
import re
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from random import randint
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import token_generator
from django.contrib import messages
from dotenv import load_dotenv
import uuid
import datetime

load_dotenv()


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url='error')
def register(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the register template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    return render(request=request, template_name='accounts/register.html', context={
        'title': 'Sign Up',
    })


def create_user(request) -> django.http.response.JsonResponse:
    """
    The function handling the registration form for a new user in the database
    using the POST method with Asynchronous JavaScript and XMLHttpRequest (AJAX) request.
    Upon successful form validation, an email message is automatically sent from the website administrator
    to the provided email address for account activation.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        username, email, raw_password1, raw_password2, terms, account_type = [data[key][0] for key in
                                                                              list(data.keys())[:-1]]
        account_type = account_type.capitalize()

        spam_verification = [data[key] for key in data][-1]
        username_field, email_field, raw_password1_field, raw_password2_field, terms_field, account_type_field = [
            data[key][1] for key in
            list(data.keys())[:-1]]
        username_label, email_label, raw_password1_label, raw_password2_label, terms_label, account_type_label = [
            data[key][2] for
            key in
            list(data.keys())[:-1]]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
            }, safe=False)

        response = [
            {
                "valid":
                    False if not username else
                    False if len(username) < 8 else
                    False if len(username) >= 8 and User.objects.filter(username=username).exists() else
                    True,
                "field": username_field,
                "message":
                    f"The {username_label} field cannot be empty." if not username else
                    f"The {username_label} should contain at least 8 characters." if len(username) < 8 else
                    f"The {username_label} already exists." if len(username) >= 8 and User.objects.filter(
                        username=username).exists() else
                    "",
            },
            {
                "valid":
                    False if not email else
                    False if not re.match(pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                          string=email) else
                    False if re.match(pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                      string=email) and User.objects.filter(email=email).exists() else
                    True,
                "field": email_field,
                "message":
                    f"The {email_label} field cannot be empty." if not email else
                    f"The {email_label} address format is invalid." if not re.match(
                        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', string=email) else
                    f"The {email_label} address {email} already exists." if re.match(
                        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                        string=email) and User.objects.filter(email=email).exists() else
                    "",
            },
            {
                "valid":
                    False if not raw_password1 else
                    False if not re.match(pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                                          string=raw_password1) else
                    True,
                "field": raw_password1_field,
                "message":
                    f"The {raw_password1_label} field cannot be empty." if not raw_password1 else
                    f"The {raw_password1_label} should be at least 8 characters long, "
                    f"including at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character." if not re.match(
                        pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                        string=raw_password1) else
                    "",
            },
            {
                "valid":
                    False if not raw_password2 else
                    False if not raw_password1 else
                    False if not re.match(pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                                          string=raw_password2) else
                    False if raw_password2 != raw_password1 else
                    True,
                "field": raw_password2_field,
                "message":
                    f"The {raw_password2_label} field cannot be empty." if not raw_password2 else
                    f"The {raw_password2_label} field must be filled in." if not raw_password1 else
                    f"The {raw_password1_label} should be at least 8 characters long, "
                    f"including at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character." if not re.match(
                        pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                        string=raw_password1) else
                    f"The {raw_password2_label} field does not match the previously entered password." if raw_password2 != raw_password1 else
                    "",
            },
            {
                "valid":
                    False if not terms else
                    True,
                "field": terms_field,
                "message":
                    "The Terms checkbox must be accepted." if not terms else
                    "",
            }
        ]

        validation = list(set([data['valid'] for data in response]))

        if len(validation) == 1:
            if validation[0]:
                if account_type == 'Individual':
                    user = User(username=username, email=email, password=make_password(password=raw_password1),
                                account_type='Individual')
                    user.save()

                    try:
                        html_message = render_to_string(template_name='accounts/activation_email.html', context={
                            'user': user,
                            'domain': get_current_site(request=request),
                            'uid': urlsafe_base64_encode(s=force_bytes(s=user.pk)),
                            'token': token_generator.make_token(user=user),
                        })
                        plain_message = strip_tags(html_message)

                        message = EmailMultiAlternatives(
                            subject='Account activation request.',
                            body=plain_message,
                            from_email=os.environ.get("EMAIL_HOST_USER"),
                            to=[user.email]
                        )

                        message.attach_alternative(content=html_message, mimetype='text/html')
                        message.send(fail_silently=True)

                        return JsonResponse(data=response, safe=False)

                    except Exception:
                        return JsonResponse(data={
                            "valid": False,
                            "message": "The message could not be sent.",
                        })
                else:
                    user = User(username=username, email=email, password=make_password(password=raw_password1),
                                account_type='Business')
                    user.save()

                    try:
                        html_message = render_to_string(template_name='accounts/activation_email.html', context={
                            'user': user,
                            'domain': get_current_site(request=request),
                            'uid': urlsafe_base64_encode(s=force_bytes(s=user.pk)),
                            'token': token_generator.make_token(user=user),
                        })
                        plain_message = strip_tags(html_message)

                        message = EmailMultiAlternatives(
                            subject='Account activation request.',
                            body=plain_message,
                            from_email=os.environ.get("EMAIL_HOST_USER"),
                            to=[user.email]
                        )

                        message.attach_alternative(content=html_message, mimetype='text/html')
                        message.send(fail_silently=True)

                        return JsonResponse(data=response, safe=False)

                    except Exception:
                        return JsonResponse(data={
                            "valid": False,
                            "message": "The message could not be sent.",
                        })


            else:
                return JsonResponse(data=response, safe=False)

        else:
            return JsonResponse(data=response, safe=False)


def activate(request, uidb64, token) -> django.http.response.HttpResponseRedirect:
    """
    The function activating the account of a new user. The activation link is valid for 5 minutes.
    Upon successful verification, the user is redirected to the login page.
    If the activation link has expired and the user has not activated the account,
    they are removed from the database and must register again.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        uidb64: str
        token: str

    Returns
    ----------
        django.http.response.HttpResponseRedirect
    """
    try:
        uid = force_str(s=urlsafe_base64_decode(s=uidb64))
        user = User.objects.get(pk=uid)
    except:
        return redirect(to=reverse(viewname='register'))

    if user and token_generator.check_token(user=user, token=token):
        user.is_verified = True
        user.save()

        return redirect(to=reverse(viewname='login'))

    else:
        user.delete()

        messages.info(request=request, message='Your activation link has expired. Please create your account again.')
        return redirect(to=reverse(viewname='register'))


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url='error')
def log_in(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the login template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    return render(request=request, template_name='accounts/login.html', context={
        'title': 'Login'
    })


def authorization(request) -> JsonResponse:
    """
    The function handles the user authentication form using the POST method with Asynchronous JavaScript
    and XMLHttpRequest (AJAX) request. Upon successful form validation, the user is logged in,
    and data such as the user's login status and their ID in the database are stored in the session.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        email, password = [data[key][0] for key in list(data.keys())[:-1]]
        spam_verification = [data[key] for key in data][-1]
        email_field, password_field = [data[key][1] for key in list(data.keys())[:-1]]
        email_label, password_label = [data[key][2] for key in list(data.keys())[:-1]]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
            }, safe=False)

        response = [
            {
                "valid":
                    False if not email else
                    False if not re.match(pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                          string=email) else
                    False if not User.objects.filter(email=email).exists() else
                    False if not User.objects.get(email=email).is_verified else
                    True,
                "field": email_field,
                "message":
                    f"The {email_label} field cannot be empty." if not email else
                    "The e-mail address format is invalid." if not re.match(
                        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', string=email) else
                    f"The e-mail {email} does not exists." if not User.objects.filter(email=email).exists() else
                    f"Your account is not yet activated. Check your email inbox"
                    f"or register again if the activation link has expired." if not User.objects.get(
                        email=email).is_verified else
                    "",
            },
            {
                "valid":
                    False if not password else
                    False if User.objects.filter(email=email).exists() and not check_password(password=password,
                                                                                              encoded=User.objects.get(
                                                                                                  email=email).password) else
                    True,
                "field": password_field,
                "message":
                    f"The {password_label} field cannot be empty." if not password else
                    f"Incorrect password for the e-mail address {email}." if User.objects.filter(
                        email=email).exists() and not check_password(password=password,
                                                                     encoded=User.objects.get(
                                                                         email=email).password) else
                    "",
            },
        ]

        validation = list(set([data['valid'] for data in response]))

        if len(validation) == 1:
            if validation[0]:
                user = authenticate(request=request, email=email, password=password,
                                    backend='django.contrib.auth.backends.ModelBackend')

                login(request=request, user=user, backend='django.contrib.auth.backends.ModelBackend')
                request.session.set_expiry(600)

                return JsonResponse(data=response, safe=False)

            else:
                return JsonResponse(data=response, safe=False)

        else:
            return JsonResponse(data=response, safe=False)


def log_out(request) -> django.http.response.HttpResponseRedirect:
    """
    Logout user.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponseRedirect
    """
    logout(request=request)

    request.session.flush()

    return redirect(to='login')


@login_required(login_url='login')
def account_settings(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the account settings template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    return render(request=request, template_name='accounts/account-settings.html', context={
        'title': 'Account Settings',
    })


def upload_avatar(request) -> django.http.response.JsonResponse:
    """
    The function handles the profile picture change form using the PATCH method
    with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the new picture is saved in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'POST':
        if request.FILES:
            file = request.FILES['file']

            if file.size > 1000000:
                return JsonResponse(data={
                    "valid": False,
                    "message": "The file size should not exceed 1 MB."
                })

            else:
                extensions = ['jpg', 'jpeg', 'webp', 'png', 'svg']

                if file.name.split(sep='.')[1] in extensions:
                    user = User.objects.get(username=request.user)
                    file.name = str(uuid.uuid4()) + '.' + file.name.split(sep='.')[1]
                    user.image = file
                    user.save()

                    return JsonResponse(data={
                        "valid": True,
                        "path": user.image.url,
                        "message": "Profile picture has been uploaded successfully.",
                    })

                return JsonResponse(data={
                    "valid": False,
                    "message": "Invalid file format. The file format should be jpg, jpeg, webp, png, svg."
                })

        else:
            return JsonResponse(data={
                "valid": False,
                "message": "No file uploaded. Please upload a file.",
            })


def user_settings(request) -> django.http.response.JsonResponse:
    """
    The function handles the user data change form, including the username, email address, and password,
    using the PATCH method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the data is updated in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'PATCH':
        data = json.loads(s=request.body.decode('utf-8'))
        username, email, raw_password1, raw_password2 = [data[key][0] for key in data]
        username_field, email_field, raw_password1_field, raw_password2_field = [data[key][1] for key in data]
        username_label, email_label, raw_password1_label, raw_password2_label = [data[key][2] for key in data]

        response = [
            {
                "valid":
                    False if len(username) < 8 and len(username) != 0 else
                    False if (len(username) > 8 and len(username) != 0) and User.objects.filter(
                        username=username).exists() else
                    True if len(username) == 0 else
                    True,
                "field": username_field,
                "value": username,
                "message":
                    "The username should contains at least 8 characters." if len(username) < 8 and len(
                        username) != 0 else
                    "The username already exists."
                    if (len(username) > 8 and len(username) != 0) and User.objects.filter(
                        username=username).exists() else
                    "" if len(username) == 0 else
                    "The username has been successfully changed.",
            },
            {
                "valid":
                    False if len(email) != 0 and not re.match(
                        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                        string=email) else
                    False if len(email) != 0 and User.objects.filter(email=email).exists() else
                    True if len(email) == 0 else
                    True,
                "field": email_field,
                "value": email,
                "message":
                    f"The {email_label} address format is invalid." if len(email) != 0 and not re.match(
                        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                        string=email) else
                    f"The {email_label} address {email} already exists." if len(email) != 0 and User.objects.filter(
                        email=email).exists() else
                    "" if len(email) == 0 else
                    "The email address has been successfully changed.",
            },
            {
                "valid":
                    False if len(raw_password1) != 0 and not re.match(
                        pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                        string=raw_password1) else
                    True if len(raw_password1) != 0 and re.match(
                        pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                        string=raw_password1) else
                    True,
                "field": raw_password1_field,
                "message":
                    f"The {raw_password1_label} should be at least 8 characters long,"
                    f"including at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character." if len(
                        raw_password1) != 0 and not re.match(
                        pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                        string=raw_password1) else
                    "The password field is valid." if len(raw_password1) != 0 and re.match(
                        pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                        string=raw_password1) else
                    "",
            },
            {
                "valid":
                    False if len(raw_password2) != 0 and not re.match(
                        pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                        string=raw_password2) else
                    False if raw_password2 != raw_password1 else
                    True,
                "field": raw_password2_field,
                "message":
                    f"The {raw_password1_label} should be at least 8 characters long, including at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character." if len(
                        raw_password2) != 0 and not re.match(
                        pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                        string=raw_password1) else
                    f"The {raw_password2_label} field does not match the previously entered password." if raw_password2 != raw_password1 else
                    "The confirm password field matches the password field." if (raw_password2 == raw_password1) and (
                            len(raw_password2) != 0 and raw_password1 != 0) else
                    "",
            },
        ]

        validation = [data['valid'] for data in response]

        result = {}

        if all(validation):
            for k, v in data.items():
                if v[0] != '':
                    result[k] = v[0]

        user = User.objects.get(username=request.user)

        for k, v in result.items():
            if k == 'password1' or k == 'password2':
                user.password = make_password(password=raw_password1)
                update_session_auth_hash(request=request, user=user)

            else:
                setattr(user, k, v)

        user.save()

        return JsonResponse(data=response, safe=False)


def profile_settings(request) -> django.http.response.JsonResponse:
    """
    The function handles the form for changing individual user profile data such as first name, last name, gender,
    and phone number, as well as the form for changing business user profile data such as company name,
    company ID, and phone number. The function utilizes the PATCH method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the data is updated in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'PATCH':
        if request.user.account_type == 'Individual':
            data = json.loads(s=request.body.decode('utf-8'))

            first_name, last_name, gender, phone_number = [data[key][0] for key in data]
            first_name_field, last_name_field, gender_field, phone_number_field = [data[key][1] for key in data]
            first_name_label, last_name_label, gender_label, phone_number_label = [data[key][2] for key in data]

            response = [
                {
                    "valid":
                        True if not first_name else
                        True,
                    "field": first_name_field,
                    "value": first_name,
                    "message":
                        "" if not first_name else
                        f"The {first_name_label} has been changed successfully.",
                },
                {
                    "valid":
                        True if not last_name else
                        True,
                    "field": last_name_field,
                    "value": last_name,
                    "message":
                        "" if not last_name else
                        f"The {last_name_label} has been changed successfully."
                },
                {
                    "valid":
                        True if gender == 'Male' else
                        True if gender == 'Female' else
                        True,
                    "field": gender_field,
                    "value": gender,
                    "message":
                        f"The {gender_label} has been changed successfully." if gender == 'Male' else
                        f"The {gender_label} has been changed successfully." if gender == 'Female' else
                        ""
                },
                {
                    "valid":
                        True if not phone_number else
                        False if not re.match(pattern="^\\+?[1-9][0-9]{7,14}$", string=phone_number) else
                        True,
                    "field": phone_number_field,
                    "value": phone_number,
                    "message":
                        "" if not phone_number else
                        f"Invalid {phone_number_label} number format." if not re.match(pattern="^\\+?[1-9][0-9]{7,14}$",
                                                                                       string=phone_number) else
                        f"The {phone_number_label} number has been changed successfully.",
                }
            ]

            result = {}

            for k, v in data.items():
                if v[0] != '':
                    result[k] = v[0]

            for k, v in result.items():
                setattr(request.user.individual, k, v)

            request.user.individual.save()

            return JsonResponse(data=response, safe=False)

        else:
            data = json.loads(s=request.body.decode('utf-8'))

            company_name, company_id, phone = [data[key][0] for key in data]
            company_name_field, company_id_field, phone_field = [data[key][1] for key in data]
            company_name_label, company_id_label, phone_label = [data[key][2] for key in data]

            response = [
                {
                    "valid":
                        True if not company_name else
                        True,
                    "field": company_name_field,
                    "value": company_name,
                    "message":
                        "" if not company_name else
                        f"The {company_name_label} has been changed successfully.",
                },
                {
                    "valid":
                        True if not company_id else
                        True,
                    "field": company_id_field,
                    "value": company_id,
                    "message":
                        "" if not company_id else
                        f"The {company_id_label} has been changed successfully.",
                },
                {
                    "valid":
                        True if not phone else
                        False if not re.match(pattern="^\\+?[1-9][0-9]{7,14}$", string=phone) else
                        True,
                    "field": phone_field,
                    "value": phone,
                    "message":
                        "" if not phone else
                        f"Invalid {phone_label} number format." if not re.match(pattern="^\\+?[1-9][0-9]{7,14}$",
                                                                                string=phone) else
                        f"The {phone_label} number has been changed successfully.",
                }
            ]

            result = {}

            for k, v in data.items():
                if v[0] != '':
                    result[k] = v[0]

            for k, v in result.items():
                setattr(request.user.business, k, v)

            request.user.business.save()

            return JsonResponse(data=response, safe=False)


def localization_settings(request) -> django.http.response.JsonResponse:
    """
    The function handles the form for changing location data in both individual and business user profiles,
    including country, state, city, street, and postal code.
    The function utilizes the PATCH method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the data is updated in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'PATCH':
        data = json.loads(s=request.body.decode('utf-8'))

        country, province, city, street, postal_code = [data[key][0] for key in data]
        country_field, province_field, city_field, street_field, postal_code_field = [data[key][1] for key in data]
        country_label, province_label, city_label, street_label, postal_code_label = [data[key][2] for key in data]

        response = [
            {
                "valid":
                    True if not country else
                    True,
                "field": country_field,
                "value": country,
                "message":
                    "" if not country else
                    f"The {country_label} has been changed successfully.",
            },
            {
                "valid":
                    True if not province else
                    True,
                "field": province_field,
                "value": province,
                "message":
                    "" if not province else
                    f"The {province_label} has been changed successfully."
            },
            {
                "valid":
                    True if not city else
                    True,
                "field": city_field,
                "value": city,
                "message":
                    "" if not city else
                    f"The {city_label} has been changed successfully.",
            },
            {
                "valid":
                    True if not street else
                    True,
                "field": street_field,
                "value": street,
                "message":
                    "" if not street else
                    f"The {street_label} has been changed successfully.",
            },
            {
                "valid":
                    True if not postal_code else
                    True,
                "field": postal_code_field,
                "value": postal_code,
                "message":
                    "" if not postal_code else
                    f"The {postal_code_label} has been changed successfully.",
            }
        ]

        result = {}

        for k, v in data.items():
            if v[0] != '':
                result[k] = v[0]

        for k, v in result.items():
            if request.user.account_type == 'Individual':
                setattr(request.user.individual, k, v)
                request.user.individual.save()
            else:
                setattr(request.user.business, k, v)
                request.user.business.save()

        return JsonResponse(data=response, safe=False)


def social_media_settings(request) -> django.http.response.JsonResponse:
    """
    The function handles the form for changing website and social media link data in both individual
    and business user profiles, including website, Facebook page, Instagram page, and LinkedIn page.
    The function utilizes the PATCH method with Asynchronous JavaScript and XMLHttpRequest (AJAX).
    Upon successful form validation, the data is updated in the database.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'PATCH':
        data = json.loads(s=request.body.decode('utf-8'))

        website_url, facebook_url, instagram_url, linkedin_url = [data[key][0] for key in data]
        website_url_field, facebook_url_field, instagram_url_field, linkedin_url_field = [data[key][1] for key in data]
        website_url_label, facebook_url_label, instagram_url_label, linkedin_url_label = [data[key][2] for key in data]

        response = [
            {
                "valid":
                    True if not website_url else
                    True,
                "field": website_url_field,
                "value": website_url,
                "message":
                    "" if not website_url else
                    f"The {website_url_label} has been changed successfully.",
            },
            {
                "valid":
                    True if not facebook_url else
                    True,
                "field": facebook_url_field,
                "value": facebook_url,
                "message":
                    "" if not facebook_url else
                    f"The {facebook_url_label} has been changed successfully.",
            },
            {
                "valid":
                    True if not instagram_url else
                    True,
                "field": instagram_url_field,
                "value": instagram_url,
                "message":
                    "" if not instagram_url else
                    f"The {instagram_url_label} has been changed successfully.",
            },
            {
                "valid":
                    True if not linkedin_url else
                    True,
                "field": linkedin_url_field,
                "value": linkedin_url,
                "message":
                    "" if not linkedin_url else
                    f"The {linkedin_url_label} has been changed successfully.",
            }
        ]

        result = {}

        for k, v in data.items():
            if v[0] != '':
                result[k] = v[0]

        for k, v in result.items():
            if request.user.account_type == 'Individual':
                setattr(request.user.individual, k, v)
                request.user.individual.save()
            else:
                setattr(request.user.business, k, v)
                request.user.business.save()

        return JsonResponse(data=response, safe=False)


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url='error')
def forget_password(request) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the forget password template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.HttpResponse
    """
    return render(request=request, template_name='accounts/forget-password.html', context={
        'title': 'Forget Password',
    })


def send_password(request) -> django.http.response.JsonResponse:
    """
    The function handling the user email address validation form using
    the POST method with Asynchronous JavaScript and XMLHttpRequest (AJAX) request.
    This function sends an email message with a OneTimePassword to the user who requests password recovery/change.
    The OneTimePassword is active for 5 minutes and stored in the session, and then deleted.
    While the OneTimePassword is active, the user cannot go back to the previous step to send another email message.
    Only after deleting the OneTimePassword from the session after 5 minutescan another password change request be sent.
    This is done to prevent potential email spam. Upon successful verification of the user's email address,
    the user is redirected to the next step for OneTimePassword validation.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        email, spam_verification = [data[key][0] for key in list(data.keys())[:-1]][0], [data[key] for key in data][1]
        email_label = [data[key][2] for key in list(data.keys())[:-1]][0]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
            })

        if request.session.get('otp'):
            now = datetime.datetime.now().time()
            expire_time = datetime.datetime.strptime(request.session['expire_time'], '%H:%M:%S').time()

            if expire_time < now:
                request.session.pop('otp')

                return JsonResponse(data={
                    "valid": False,
                    "message": f"The previous password has expired. "
                               f"Click 'Reset Password' to receive a new password at the email address {email}.",
                })

            else:
                return JsonResponse(data={
                    "valid": True,
                    "email": email,
                })

        else:
            request.session['otp'] = str(randint(a=1111, b=9999))
            request.session['expire_time'] = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime(
                '%H:%M:%S')

            if email:
                if re.match(pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', string=email):
                    if User.objects.filter(email=email).exists():
                        user = User.objects.get(email=email)

                        try:
                            html_message = render_to_string(template_name='accounts/password_reset_email.html',
                                                            context={
                                                                'one_time_password': request.session['otp'],
                                                                'expire_password': request.session['expire_time'],
                                                            })
                            plain_message = strip_tags(html_message)

                            message = EmailMultiAlternatives(
                                subject=f"Password reset request for {user.username}.",
                                body=plain_message,
                                from_email=os.environ.get("EMAIL_HOST_USER"),
                                to=[user.email]
                            )

                            message.attach_alternative(content=html_message, mimetype='text/html')
                            message.send(fail_silently=True)

                            return JsonResponse(data={
                                "valid": True,
                                "email": email,
                                "message": "",
                            })

                        except Exception:
                            return JsonResponse(data={
                                "valid": False,
                                "message": "The message could not be sent.",
                            })

                    else:
                        return JsonResponse(data={
                            "valid": False,
                            "message": "The user with the provided email address does not exist.",
                        })

                else:
                    return JsonResponse(data={
                        "valid": False,
                        "message": f"The {email_label} address format is invalid.",
                    })

            else:
                return JsonResponse(data={
                    "valid": False,
                    "message": f"The {email_label} field cannot be empty.",
                })


def validate_password(request) -> django.http.response.JsonResponse:
    """
    The function handling the OneTimePassword validation form using
    the POST method with Asynchronous JavaScript and XMLHttpRequest (AJAX) request.
    The one-time password is stored in the session; during validation,
    the password entered by the user is compared with the password stored in the session
    and sent to the provided email address. Upon successful form validation,
    the user can proceed to set a new password for their account.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))
        password, email, spam_verification = [data[key] for key in data]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
            })

        if password:
            token = request.session['otp']

            if password == token:
                return JsonResponse(data={
                    "valid": True,
                    "email": email,
                    "message": "",
                }, safe=False)

            else:
                return JsonResponse(data={
                    "valid": False,
                    "message": "Invalid code.",
                }, safe=False)

        else:
            return JsonResponse(data={
                "valid": False,
                "message": "Fill all inputs.",
            }, safe=False)


def set_password(request) -> django.http.response.JsonResponse:
    """
    The function handling the user password update form and saving it to the database
    using the PATCH method with Asynchronous JavaScript and XMLHttpRequest (AJAX) request.
    Upon successful form validation, the database is automatically updated with the new password,
    and the session storing the one-time password and its expiration time is deleted.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest

    Returns
    ----------
        django.http.response.JsonResponse
    """
    if request.method == 'PATCH':
        data = json.loads(s=request.body.decode('utf-8'))

        raw_password1, raw_password2 = [data[key][0] for key in list(data.keys())[:-2]]
        raw_password1_field, raw_password2_field = [data[key][1] for key in list(data.keys())[:-2]]
        raw_password1_label, raw_password2_label = [data[key][2] for key in list(data.keys())[:-2]]

        email = [data[key] for key in data][-2]
        spam_verification = [data[key] for key in data][-1]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
            })

        response = [
            {
                "valid":
                    False if not raw_password1 else
                    False if not re.match(pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                                          string=raw_password1) else
                    True,
                "field": raw_password1_field,
                "message":
                    f"The {raw_password1_label} field cannot be empty." if not raw_password1 else
                    f"The {raw_password1_label} should be at least 8 characters long,"
                    f"including at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character." if not re.match(
                        pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                        string=raw_password1) else
                    "",
            },
            {
                "valid":
                    False if not raw_password2 else
                    False if not raw_password1 else
                    False if not re.match(pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                                          string=raw_password2) else
                    False if raw_password2 != raw_password1 else
                    True,
                "field": raw_password2_field,
                "message":
                    f"The {raw_password2_label} field cannot be empty." if not raw_password2 else
                    f"The {raw_password1_label} field must be filled in." if not raw_password1 else
                    f"The {raw_password1_label} should be at least 8 characters long, including at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character." if not re.match(
                        pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                        string=raw_password1) else
                    f"The {raw_password2_label} field does not match the previously entered password." if raw_password2 != raw_password1 else
                    "",
            },
        ]

        validation = list(set([data['valid'] for data in response]))

        if len(validation) == 1:
            if validation[0]:
                user = User.objects.get(email=email)
                user.set_password(raw_password=raw_password1)
                user.save()

                request.session.pop('otp')
                request.session.pop('expire_time')

                return JsonResponse(data=response, safe=False)

            else:
                return JsonResponse(data=response, safe=False)

        else:
            return JsonResponse(data=response, safe=False)


def account_details(request, username) -> django.http.response.HttpResponse:
    """
    Returns an HttpResponse with the account details template.

    Parameters
    ----------
        request: django.core.handlers.wsgi.WSGIRequest
        username: str

    Returns
    ----------
        django.http.response.HttpResponse
    """
    u = User.objects.get(username=username)

    if u.account_type == 'Individual':
        profile = Individual.objects.get(user=u)

    else:
        profile = Business.objects.get(user=u)

    return render(request=request, template_name='accounts/account-details.html', context={
        'title': 'Account Details',
        'u': u,
        'profile': profile,
    })
