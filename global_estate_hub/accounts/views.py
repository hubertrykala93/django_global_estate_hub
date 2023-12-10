import os
from django.shortcuts import render, redirect, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from .models import User, OneTimePassword
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

load_dotenv()


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url='error')
def register(request):
    """
    Returns an HttpResponse with the register template.

    return: HttpResponse
    """
    return render(request=request, template_name='accounts/register.html', context={
        'title': 'Sign Up',
    })


def create_user(request):
    """
    The function handling the registration form for a new user in the database
    using the POST method with Asynchronous JavaScript and XML (AJAX) request.
    Upon successful form validation, an email message is automatically sent from the website administrator
    to the provided email address for account activation.

    return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        username, email, raw_password1, raw_password2, terms, account_type = [data[key][0] for key in
                                                                              list(data.keys())[:-1]]
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
                    "The username should contain at least 8 characters." if len(username) < 8 else
                    "The username already exists." if len(username) >= 8 and User.objects.filter(
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
                    "The e-mail address format is invalid." if not re.match(
                        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', string=email) else
                    f"The e-mail address {email} already exists." if re.match(
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
                    "The password should be at least 8 characters long, including at least one uppercase letter, "
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
                    "The password should be at least 8 characters long, including at least one uppercase letter, "
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
        print(validation)

        if len(validation) == 1:
            if validation[0]:
                if account_type == 'individual':
                    user = User(username=username, email=email, password=make_password(password=raw_password1),
                                is_individual=True, is_business=False)
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
                                is_individual=False, is_business=True)
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


def activate(request, uidb64, token):
    """
    The function activating the account of a new user. The activation link is valid for 5 minutes.
    Upon successful verification, the user is redirected to the login page.
    If the activation link has expired and the user has not activated the account,
    they are removed from the database and must register again.

    return: HttpResponseRedirect
    """
    try:
        uid = force_str(s=urlsafe_base64_decode(s=uidb64))
        user = User.objects.get(pk=uid)
    except:
        return redirect(to=reverse(viewname='register'))

    if user and token_generator.check_token(user=user, token=token):
        user.is_verified = True
        user.save()

        messages.success(request=request, message='Congratulations, your account has been activated.')

        return redirect(to=reverse(viewname='login'))

    else:
        user.delete()

        messages.info(request=request, message='Your activation link has expired. Please create your account again.')
        return redirect(to=reverse(viewname='register'))


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url='error')
def log_in(request):
    """
    Returns an HttpResponse with the login template.
    """
    return render(request=request, template_name='accounts/login.html', context={
        'title': 'Login'
    })


def authorization(request):
    """
    The function handling the user authentication form using
    the POST method with Asynchronous JavaScript and XML (AJAX) request.
    Upon successful form validation, the user is logged in.

    return: JsonResponse
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

                return JsonResponse(data=response, safe=False)

            else:
                return JsonResponse(data=response, safe=False)

        else:
            return JsonResponse(data=response, safe=False)


def log_out(request):
    """
    Logout user.

    return: HttpResponseRedirect
    """
    logout(request=request)

    return redirect(to='login')


@login_required(login_url='login')
def account_settings(request):
    """
    Returns an HttpResponse with the account settings template.

    return: HttpResponse
    """
    return render(request=request, template_name='accounts/account-settings.html', context={
        'title': 'Account Settings',
    })


def upload_avatar(request):
    """
    The function handles the profile picture change form using the PATCH method
    with Asynchronous JavaScript and XML (AJAX).
    Upon successful form validation, the new picture is saved in the database.

    return: JsonResponse
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


def user_settings(request):
    pass


def profile_settings(request):
    pass


def localization_settings(request):
    pass


def social_media_settings(request):
    pass


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url='error')
def forget_password(request):
    """
    Returns an HttpResponse with the forget password template.

    return: HttpResponse
    """
    return render(request=request, template_name='accounts/forget-password.html', context={
        'title': 'Forget Password',
    })


def send_password(request):
    """
    The function handling the user email address validation form using
    the POST method with Asynchronous JavaScript and XML (AJAX) request.

    This function sends an email message with a OneTimePassword to the user who requests password recovery/change.
    The OneTimePassword is active for 5 minutes and then deleted. While the OneTimePassword is active,
    the user cannot go back to the previous step to send another email message.
    Only after deleting the OneTimePassword from the database can another password change request be sent.
    This is done to prevent potential email spam. Upon successful verification of the user's email address,
    the user is redirected to the next step for OneTimePassword validation.

    return: JsonResponse
    """
    if request.method == 'POST':
        one_time_password = randint(a=1111, b=9999)
        data = json.loads(s=request.body.decode('utf-8'))

        email, spam_verification = [data[key][0] for key in list(data.keys())[:-1]][0], [data[key] for key in data][1]
        email_label = [data[key][2] for key in list(data.keys())[:-1]][0]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
            })

        if email:
            if re.match(pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', string=email):
                if User.objects.filter(email=email).exists():
                    if len(OneTimePassword.objects.filter(user_id=User.objects.get(email=email).pk)) == 0:
                        user = User.objects.get(email=email)
                        one_time_password = OneTimePassword(user=user, password=one_time_password)
                        one_time_password.save()

                        try:
                            html_message = render_to_string(template_name='accounts/password_reset_email.html',
                                                            context={
                                                                'one_time_password': one_time_password.password,
                                                                'expire_password': one_time_password.expires_in,
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

                    elif len(OneTimePassword.objects.filter(user_id=User.objects.get(email=email).pk)) == 1:
                        return JsonResponse(data={
                            "valid": True,
                            "email": email,
                        })

                else:
                    return JsonResponse(data={
                        "valid": False,
                        "message": "The user with the provided email address does not exist.",
                    })

            else:
                return JsonResponse(data={
                    "valid": False,
                    "message": "The e-mail address format is invalid.",
                })

        else:
            return JsonResponse(data={
                "valid": False,
                "message": f"The {email_label} field cannot be empty.",
            })


def validate_password(request):
    """
    The function handling the OneTimePassword validation form using
    the POST method with Asynchronous JavaScript and XML (AJAX) request.
    Upon successful form validation, the user can proceed to set a new password for their account.

    return: JsonResponse
    """
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))
        password, email, spam_verification = [data[key] for key in data]

        if len(spam_verification) != 0:
            return JsonResponse(data={
                "valid": None,
            })

        if password:
            user_id = User.objects.get(email=email).pk
            token = OneTimePassword.objects.get(user_id=user_id).password

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


def set_password(request):
    """
    The function handling the user password update form and saving it to the database
    using the PATCH method with Asynchronous JavaScript and XML (AJAX) request.
    Upon successful form validation, the database is automatically updated.

    return: JsonResponse
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
                user_id = User.objects.get(email=email).pk
                user.set_password(raw_password=raw_password1)
                user.save()

                password = OneTimePassword.objects.get(user_id=user_id)
                password.delete()

                return JsonResponse(data=response, safe=False)

            else:
                return JsonResponse(data=response, safe=False)

        else:
            return JsonResponse(data=response, safe=False)
