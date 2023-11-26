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
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import token_generator
from django.contrib import messages
from dotenv import load_dotenv

load_dotenv()


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url='error')
def register(request):
    return render(request=request, template_name='accounts/register.html', context={
        'title': 'Sign Up',
    })


def create_user(request):
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        username, email, raw_password1, raw_password2, terms = [data[key][0] for key in data]
        username_field, email_field, raw_password1_field, raw_password2_field, terms_field = [data[key][1] for key in
                                                                                              data]

        response = [
            {
                "valid":
                    False if not username else
                    False if not re.match(pattern='^[a-zA-Z0-9_.-]+$', string=username) else
                    False if re.match(pattern='^[a-zA-Z0-9_.-]+$', string=username) and User.objects.filter(
                        username=username).exists() else
                    True,
                "field": username_field,
                "message":
                    "The username field cannot be empty." if not username else
                    "The username must consist only of lowercase/uppercase letters, digits or '.', '_', '-'." if not re.match(
                        pattern='^[a-zA-Z0-9_.-]+$', string=username) else
                    "The username already exists." if re.match(pattern='^[a-zA-Z0-9_.-]+$',
                                                               string=username) and User.objects.filter(
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
                    "The e-mail field cannot be empty." if not email else
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
                    "The password cannot be empty." if not raw_password1 else
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
                    "The confirm password field cannot be empty." if not raw_password2 else
                    "The password field must be filled in." if not raw_password1 else
                    "The password should be at least 8 characters long, including at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character." if not re.match(
                        pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                        string=raw_password1) else
                    "The confirm password field does not match the previously entered password." if raw_password2 != raw_password1 else
                    "",
            },
            {
                "valid":
                    False if not terms else
                    True,
                "field": terms_field,
                "message":
                    "The Terms & Privacy policy must be accepted." if not terms else
                    "",
            }
        ]

        validation = list(set([data['valid'] for data in response]))

        if len(validation) == 1:
            if validation[0]:
                user = User(username=username, email=email, password=make_password(password=raw_password1))
                # user.save()

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
                    # message.send(fail_silently=True)

                    messages.info(request=request, message=f"The activation link has been sent to {email}.")

                    return JsonResponse(data=response, safe=False)

                except BadHeaderError:
                    return JsonResponse(data={
                        "valid": False,
                        "message": "The message could not be sent.",
                    })

            else:
                return JsonResponse(data=response, safe=False)

        else:
            return JsonResponse(data=response, safe=False)


def activate(request, uidb64, token):
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
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        email, password = [data[key][0] for key in data]
        email_field, password_field = [data[key][1] for key in data]

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
                    "The e-mail field cannot be empty." if not email else
                    "The e-mail address format is invalid." if not re.match(
                        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', string=email) else
                    f"The e-mail {email} does not exists." if not User.objects.filter(email=email).exists() else
                    f"Your account has not been activated yet. Check your inbox." if not User.objects.get(
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
                    "The password field cannot be empty." if not password else
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

    return render(request=request, template_name='accounts/login.html', context={
        'title': 'Login'
    })


def log_out(request):
    logout(request=request)

    return redirect(to='login')


@login_required(login_url='login')
def account_settings(request):
    return render(request=request, template_name='accounts/account-settings.html', context={
        'title': 'Account Settings',
    })


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url='error')
def forget_password(request):
    return render(request=request, template_name='accounts/forget-password.html', context={
        'title': 'Forget Password',
    })


def send_password(request):
    if request.method == 'POST':
        one_time_password = randint(a=1111, b=9999)
        data = json.loads(s=request.body.decode('utf-8'))
        email = data['email']

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
                            }, safe=False)

                        except BadHeaderError:
                            return JsonResponse(data={
                                "valid": False,
                                "message": "The message could not be sent.",
                            })

                    elif len(OneTimePassword.objects.filter(user_id=User.objects.get(email=email).pk)) == 1:
                        return JsonResponse(data={
                            "valid": True,
                            "email": email,
                            "message": "",
                        }, safe=False)

                else:
                    return JsonResponse(data={
                        "valid": False,
                        "message": "The user with the provided email address does not exist.",
                    }, safe=False)

            else:
                return JsonResponse(data={
                    "valid": False,
                    "message": "The e-mail address format is invalid.",
                }, safe=False)

        else:
            return JsonResponse(data={
                "valid": False,
                "message": "The e-mail field cannot be empty.",
            }, safe=False)


def validate_password(request):
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))
        password = data['code']
        email = data['email']

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
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        raw_password1_field, raw_password2_field = [data[key][1] for key in list(data.keys())[:-1]]

        raw_password1 = data['password1'][0]
        raw_password2 = data['password2'][0]

        email = data['email']

        response = [
            {
                "valid":
                    False if not raw_password1 else
                    False if not re.match(pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                                          string=raw_password1) else
                    True,
                "field": raw_password1_field,
                "message":
                    "The password cannot be empty." if not raw_password1 else
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
                    "The confirm password field cannot be empty." if not raw_password2 else
                    "The password field must be filled in." if not raw_password1 else
                    "The password should be at least 8 characters long, including at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character." if not re.match(
                        pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                        string=raw_password1) else
                    "The confirm password field does not match the previously entered password." if raw_password2 != raw_password1 else
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
