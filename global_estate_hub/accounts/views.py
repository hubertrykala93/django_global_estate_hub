from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from .models import User
import json
import re


def register(request):
    return render(request=request, template_name='accounts/register.html', context={
        'title': 'Sign Up',
    })


def create_user(request):
    if request.method == 'POST':
        data = json.loads(s=request.body.decode('utf-8'))

        username = data['userName'][0]
        username_field = data['userName'][1]

        email = data['email'][0]
        email_field = data['email'][1]

        raw_password1 = data['password1'][0]
        password1_field = data['password1'][1]

        raw_password2 = data['password2'][0]
        password2_field = data['password2'][1]

        if username:
            if re.match(pattern='^[a-zA-Z0-9_.-]+$', string=username):
                if not User.objects.filter(username=username).exists():
                    if email:
                        if re.match(pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$', string=email):
                            if not User.objects.filter(email=email).exists():
                                if raw_password1:
                                    if re.match(
                                            pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                                            string=raw_password1):
                                        if raw_password2:
                                            if raw_password1 == raw_password2:
                                                password = make_password(password=raw_password1)

                                                new_user = User(username=username, email=email,
                                                                password=make_password(password=password))
                                                new_user.save()

                                                return JsonResponse(data={
                                                    "data": [
                                                        {
                                                            "valid": True,
                                                            "username": username,
                                                            "username_field": username_field,
                                                            "email": email,
                                                            "email_field": email_field,
                                                            "password1": password,
                                                            "password1_field": password1_field,
                                                            "password2": password,
                                                            "password2_field": password2_field,
                                                            "message": "The account has been successfully created",
                                                        }
                                                    ]
                                                })
                                            else:
                                                return JsonResponse(data={
                                                    "password2": [
                                                        {
                                                            "valid": False,
                                                            "password2": make_password(password=raw_password2),
                                                            "password2_field": password2_field,
                                                            "message": "The confirm password field does not match "
                                                                       "the previously entered password."
                                                        }
                                                    ]
                                                })
                                        else:
                                            return JsonResponse(data={
                                                "password2": [
                                                    {
                                                        "valid": False,
                                                        "password2": make_password(password=raw_password2),
                                                        "password2_field": password2_field,
                                                        "message": "The confirm password field cannot be empty.",
                                                    }
                                                ]
                                            })

                                    else:
                                        return JsonResponse(data={
                                            "password1": [
                                                {
                                                    "valid": False,
                                                    "password1": make_password(password=raw_password1),
                                                    "password1_field": password1_field,
                                                    "message": "The password should be at least 8 characters long, "
                                                               "including at least one uppercase letter, "
                                                               "one lowercase letter, one digit, "
                                                               "and one special character.",
                                                }
                                            ]
                                        })
                                else:
                                    return JsonResponse(data={
                                        "password1": [
                                            {
                                                "valid": False,
                                                "password1": make_password(password=raw_password1),
                                                "password1_field": password1_field,
                                                "message": "The password field cannot be empty.",
                                            }
                                        ]
                                    })
                            else:
                                return JsonResponse(data={
                                    "email": [
                                        {
                                            "valid": False,
                                            "email": email,
                                            "email_field": email_field,
                                            "message": "The e-mail address already exists.",
                                        }
                                    ]
                                })
                        else:
                            return JsonResponse(data={
                                "email": [
                                    {
                                        "valid": False,
                                        "email": email,
                                        "email_field": email_field,
                                        "message": "The e-mail address format is invalid.",
                                    }
                                ]
                            })
                    else:
                        return JsonResponse(data={
                            "email": [
                                {
                                    "valid": False,
                                    "email": email,
                                    "email_field": email_field,
                                    "message": "The e-mail field cannot be empty.",
                                }
                            ]
                        })
                else:
                    return JsonResponse(data={
                        "userName": [
                            {
                                "valid": False,
                                "username": username,
                                "username_field": username_field,
                                "message": "The username already exists.",
                            }
                        ]
                    })
            else:
                return JsonResponse(data={
                    "userName": [
                        {
                            "valid": False,
                            "username": username,
                            "username_field": username_field,
                            "message": "The username must consist only of lowercase/uppercase "
                                       "letters, digits or '.', '_', '-'.",
                        }
                    ]
                })
        else:
            return JsonResponse(data={
                "userName": [
                    {
                        "valid": False,
                        "username": username,
                        "username_field": username_field,
                        "message": "The username field cannot be empty.",
                    }
                ]
            })

    else:
        return JsonResponse(data={
            "valid": False,
            "message": "It is not possible to register a new user.",
        })


def login(request):
    return render(request=request, template_name='accounts/login.html', context={
        'title': 'Login'
    })


def logout(request):
    pass
