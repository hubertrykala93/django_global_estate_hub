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

        password1 = data['password1'][0]
        # password1 = make_password(password=data['password1'][0])
        password1_field = data['password1'][1]

        password2 = data['password2'][0]
        # password2 = make_password(password=data['password2'][0])
        password2_field = data['password2'][1]

        if not username:
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

        if not email:
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

        if not password1:
            return JsonResponse(data={
                "password1": [
                    {
                        "valid": False,
                        "password1": password1,
                        "password1_field": password1_field,
                        "message": "The password field cannot be empty.",
                    }
                ]
            })

        if not password2:
            return JsonResponse(data={
                "password2": [
                    {
                        "valid": False,
                        "password2": password2,
                        "password2_field": password2_field,
                        "message": "The confirm password field cannot be empty."
                    }
                ]
            })

        else:
            if username:
                if re.match(pattern='^[a-zA-Z0-9_.-]+$', string=username):
                    if not User.objects.filter(username=username).exists():
                        if email:
                            if re.match(pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$', string=email):
                                if not User.objects.filter(email=email).exists():
                                    if password1:
                                        if re.match(
                                                pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$',
                                                string=password1):
                                            if password2:
                                                if password1 == password2:
                                                    new_user = User(username=username, email=email, password=password1)
                                                    new_user.save()

                                                    return JsonResponse(data={
                                                        "data": [
                                                            {
                                                                "valid": True,
                                                                "message": "The account has been successfully created",
                                                            }
                                                        ]
                                                    })
                                else:
                                    return JsonResponse(data={
                                        "email": [
                                            {
                                                "valid": False,
                                                "message": "The e-mail address already exists.",
                                            }
                                        ]
                                    })
                            else:
                                return JsonResponse(data={
                                    "email": [
                                        {
                                            "valid": False,
                                            "message": "The e-mail address is invalid.",
                                        }
                                    ]
                                })
                    else:
                        return JsonResponse(data={
                            "userName": [
                                {
                                    "valid": False,
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
            "valid": False,
            "message": "It is not possible to register a new user.",
        })


def login(request):
    return render(request=request, template_name='accounts/login.html', context={
        'title': 'Login'
    })


def logout(request):
    pass
