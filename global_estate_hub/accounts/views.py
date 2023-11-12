import os
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from .models import User, OneTimePassword
import json
import re
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from random import randint
from django.core.mail import BadHeaderError, EmailMessage
from django.template.loader import render_to_string
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

        username = data['userName'][0]
        email = data['email'][0]
        raw_password1 = data['password1'][0]
        raw_password2 = data['password2'][0]
        terms = data['terms'][0]

        username_field = data['userName'][1]
        email_field = data['email'][1]
        raw_password1_field = data['password1'][1]
        raw_password2_field = data['password2'][1]
        terms_field = data['terms'][1]

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
                    "Correct username.",
            },
            {
                "valid":
                    False if not email else
                    False if not re.match(pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$', string=email) else
                    False if re.match(pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$',
                                      string=email) and User.objects.filter(email=email).exists() else
                    True,
                "field": email_field,
                "message":
                    "The e-mail field cannot be empty." if not email else
                    "The e-mail address format is invalid." if not re.match(
                        pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$', string=email) else
                    "The e-mail address already exists." if re.match(
                        pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$',
                        string=email) and User.objects.filter(email=email).exists() else
                    "Correct e-mail address.",
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
                    "Correct password.",
            },
            {
                "valid":
                    False if not raw_password2 else
                    False if not raw_password1 else
                    False if raw_password2 != raw_password1 else
                    True,
                "field": raw_password2_field,
                "message":
                    "The confirm password field cannot be empty." if not raw_password2 else
                    "The password field must be filled in." if not raw_password1 else
                    "The confirm password field does not match the previously entered password." if raw_password2 != raw_password1 else
                    "Correct password confirmation.",
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

        if list(set([data['valid'] for data in response]))[0]:
            user = User(username=username, email=email, password=make_password(password=raw_password1))
            user.save()

            return JsonResponse(data=response, safe=False)

        else:
            return JsonResponse(data=response, safe=False)


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url='error')
def log_in(request):
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        email = data['email'][0]
        password = data['password'][0]

        email_field = data['email'][1]
        password_field = data['password'][1]

        response = [
            {
                "valid":
                    False if not email else
                    False if not User.objects.filter(email=email).exists() else
                    True,
                "field": email_field,
                "message":
                    "The e-mail field cannot be empty." if not email else
                    f"The e-mail {email} does not exists." if not User.objects.filter(email=email).exists() else
                    "Correct e-mail address.",
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
                    True,
            },
        ]

        if list(set([data['valid'] for data in response]))[0]:
            user = authenticate(request=request, email=email, password=password,
                                backend='django.contrib.auth.backends.ModelBackend')
            login(request=request, user=user, backend='django.contrib.auth.backends.ModelBackend')

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


def send_otp(request):
    if request.method == 'POST':
        one_time_password = randint(a=1111, b=9999)
        data = json.loads(s=request.body.decode('utf-8'))
        email = data['email']

        if email:
            if User.objects.filter(email=email).exists():
                if len(OneTimePassword.objects.filter(user_id=User.objects.get(email=email).pk)) == 0:
                    user = User.objects.get(email=email)
                    one_time_password = OneTimePassword(user=user, password=one_time_password)
                    one_time_password.save()

                    try:
                        message = EmailMessage(
                            subject=f"Password reset request for {user.username}.",
                            body=render_to_string(template_name='accounts/password_reset_email.html', context={
                                'one_time_password': one_time_password.password,
                                'expire_password': one_time_password.expires_in,
                            }),
                            from_email=os.environ.get("EMAIL_HOST_USER"),
                            to=[user.email]
                        )

                        message.send(fail_silently=True)

                        return JsonResponse(data={
                            "valid": True,
                            "email": email,
                            "message": "",
                        }, safe=False)

                    except BadHeaderError:
                        return JsonResponse(data={
                            "valid": False,
                            "email": email,
                            "message": "The message could not be sent.",
                        })

                elif len(OneTimePassword.objects.filter(user_id=User.objects.get(email=email).pk)) == 1:
                    return JsonResponse(data={
                        "valid": True,
                        "email": email,
                        "message": "The code is already assigned to this user. Check your inbox. "
                                   "The token is valid for 5 minutes.",
                    }, safe=False)

            else:
                return JsonResponse(data={
                    "valid": False,
                    "message": "The user with the provided email address does not exist.",
                }, safe=False)

        else:
            return JsonResponse(data={
                "valid": False,
                "message": "The e-mail field cannot be empty.",
            }, safe=False)


def check_otp(request):
    pass
