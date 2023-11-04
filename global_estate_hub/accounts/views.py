from django.shortcuts import render
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

        # if not username and email and password1 and password2:
        #     return JsonResponse(data={
        #         "userName": [
        #             {
        #                 "valid": False,
        #                 "username": username,
        #                 "username_field": username_field,
        #                 "message": "The username field cannot be empty."
        #             }
        #         ]
        #     })

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

        elif not email:
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

        elif not password1:
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

        elif not password2:
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

        if username:
            if re.match(pattern='^[a-zA-Z0-9_.-]+$', string=username):
                return JsonResponse(data={
                    "userName": [
                        {
                            "valid": True,
                            "username": username,
                            "username_field": username_field,
                            "message": "The username is valid."
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
                                       "letters, digits or '.', '_', '-'."
                        }
                    ]
                })

        else:
            pass

        if email:
            if re.match(pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$', string=email):
                return JsonResponse(data={
                    "email": [
                        {
                            "valid": True,
                            "email": email,
                            "email_field": email_field,
                            "message": "The e-mail address is valid."
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
                            "message": "Invalid email address format."
                        }
                    ]
                })

        else:
            pass

        if password1:
            pass

        else:
            return JsonResponse(data={
                "password1": [
                    {
                        "valid": False,
                        "password1": password1,
                        "password1_field": password1_field,
                        "message": "The password field cannot be empty."
                    }
                ]
            })

        if password2:
            pass

        else:
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
