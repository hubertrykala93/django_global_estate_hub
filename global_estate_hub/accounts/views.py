from django.shortcuts import render
from django.contrib.auth.hashers import make_password
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
        email = data['email'][0]
        raw_password1 = data['password1'][0]
        raw_password2 = data['password2'][0]

        print(username)
        print(email)
        print(raw_password1)
        print(raw_password2)

        messages = [
            "The account has been successfully created. You can now login.",

            "The confirm password field does not match the previously entered password.",

            "The password should be at least 8 characters long, including at least one uppercase letter, "
            "one lowercase letter, one digit, and one special character.",

            "The e-mail address already exists.",

            "The e-mail address format is invalid.",

            "The username must consist only of lowercase/uppercase letters, digits or '.', '_', '-'."
        ]

        username_pattern = '^[a-zA-Z0-9_.-]+$'
        email_pattern = '^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'
        password_pattern = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'

        if not username and not email and not raw_password1 and not raw_password2:
            return JsonResponse(data=[
                {
                    "valid": False,
                    "field": "userName",
                    "message": "The username cannot be empty.",
                },
                {
                    "valid": False,
                    "field": "email",
                    "message": "The e-mail field cannot be empty.",
                },
                {
                    "valid": False,
                    "field": "password1",
                    "message": "The password field cannot be empty.",
                },
                {
                    "valid": False,
                    "field": "password2",
                    "message": "The confirm password field cannot be empty.",
                }
            ], safe=False)

        if username and not email and not raw_password1 and not raw_password1:
            if re.match(pattern='^[a-zA-Z0-9_.-]+$', string=username):
                if not User.objects.filter(username=username).exists():
                    return JsonResponse(data=[
                        {
                            "valid": True,
                            "field": "userName",
                            "message": "The username is valid.",
                        },
                        {
                            "valid": False,
                            "field": "email",
                            "message": "The email field cannot be empty.",
                        },
                        {
                            "valid": False,
                            "field": "password1",
                            "message": "The password field cannot be empty.",
                        },
                        {
                            "valid": False,
                            "field": "password2",
                            "message": "The confirm password field cannot be empty.",
                        }
                    ], safe=False)
                else:
                    return JsonResponse(data=[
                        {
                            "valid": False,
                            "field": "userName",
                            "message": "The username already exists.",
                        },
                        {
                            "valid": False,
                            "field": "email",
                            "message": "The email field cannot be empty.",
                        },
                        {
                            "valid": False,
                            "field": "password1",
                            "message": "The password field cannot be empty.",
                        },
                        {
                            "valid": False,
                            "field": "password2",
                            "message": "The confirm password field cannot be empty.",
                        }
                    ], safe=False)

            else:
                return JsonResponse(data=[
                    {
                        "valid": False,
                        "field": "userName",
                        "message": "The username must consist only of lowercase/uppercase letters, "
                                   "digits or '.', '_', '-'.",
                    },
                    {
                        "valid": False,
                        "field": "email",
                        "message": "The email field cannot be empty.",
                    },
                    {
                        "valid": False,
                        "field": "password1",
                        "message": "The password field cannot be empty.",
                    },
                    {
                        "valid": False,
                        "field": "password2",
                        "message": "The confirm password field cannot be empty.",
                    }
                ], safe=False)

        if not username and email and not raw_password1 and not raw_password2:
            if re.match(pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$', string=email):
                if not User.objects.filter(email=email).exists():
                    return JsonResponse(data=[
                        {
                            "valid": False,
                            "field": "userName",
                            "message": "The username field cannot be empty.",
                        },
                        {
                            "valid": True,
                            "field": "email",
                            "message": "The e-mail is valid.",
                        },
                        {
                            "valid": False,
                            "field": "password1",
                            "message": "The password field cannot be empty.",
                        },
                        {
                            "valid": False,
                            "field": "password2",
                            "message": "The confirm password field cannot be empty.",
                        }
                    ], safe=False)
                else:
                    return JsonResponse(data=[
                        {
                            "valid": False,
                            "field": "userName",
                            "message": "The username field cannot be empty.",
                        },
                        {
                            "valid": True,
                            "field": "email",
                            "message": "The e-mail address already exists.",
                        },
                        {
                            "valid": False,
                            "field": "password1",
                            "message": "The password field cannot be empty.",
                        },
                        {
                            "valid": False,
                            "field": "password2",
                            "message": "The confirm password field cannot be empty.",
                        }
                    ], safe=False)
            else:
                return JsonResponse(data=[
                    {
                        "valid": False,
                        "field": "userName",
                        "message": "The username field cannot be empty.",
                    },
                    {
                        "valid": True,
                        "field": "email",
                        "message": "The e-mail address format is invalid.",
                    },
                    {
                        "valid": False,
                        "field": "password1",
                        "message": "The password field cannot be empty.",
                    },
                    {
                        "valid": False,
                        "field": "password2",
                        "message": "The confirm password field cannot be empty.",
                    }
                ], safe=False)

        if not username and not email and raw_password1 and not raw_password2:
            if re.match(pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', string=raw_password1):
                return JsonResponse(data=[
                    {
                        "valid": False,
                        "field": "userName",
                        "message": "The username field cannot be empty.",
                    },
                    {
                        "valid": True,
                        "field": "email",
                        "message": "The e-mail field cannot be empty.",
                    },
                    {
                        "valid": False,
                        "field": "password1",
                        "message": "The password is valid.",
                    },
                    {
                        "valid": False,
                        "field": "password2",
                        "message": "The confirm password field cannot be empty.",
                    }
                ], safe=False)
            else:
                return JsonResponse(data=[
                    {
                        "valid": False,
                        "field": "userName",
                        "message": "The username field cannot be empty.",
                    },
                    {
                        "valid": True,
                        "field": "email",
                        "message": "The e-mail address cannot be empty.",
                    },
                    {
                        "valid": False,
                        "field": "password1",
                        "message": "The password should be at least 8 characters long, including"
                                   " at least one uppercase letter, one lowercase letter, one digit, "
                                   "and one special character.",
                    },
                    {
                        "valid": False,
                        "field": "password2",
                        "message": "The confirm password field cannot be empty.",
                    }
                ], safe=False)

        if not username and not email and not raw_password1 and raw_password2:
            if re.match(pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', string=raw_password2):
                return JsonResponse(data=[
                    {
                        "valid": False,
                        "field": "userName",
                        "message": "The username field cannot be empty.",
                    },
                    {
                        "valid": False,
                        "field": "email",
                        "message": "The e-mail field cannot be empty.",
                    },
                    {
                        "valid": False,
                        "field": "password1",
                        "message": "The password field cannot be empty.",
                    },
                    {
                        "valid": True,
                        "field": "password2",
                        "message": "The confirm password is valid but does not match the previously entered password, "
                                   "which is empty.",
                    }
                ], safe=False)

            else:
                return JsonResponse(data=[
                    {
                        "valid": False,
                        "field": "userName",
                        "message": "The username field cannot be empty.",
                    },
                    {
                        "valid": False,
                        "field": "email",
                        "message": "The e-mail field cannot be empty.",
                    },
                    {
                        "valid": False,
                        "field": "password1",
                        "message": "The password field cannot be empty.",
                    },
                    {
                        "valid": False,
                        "field": "password2",
                        "message": "The password should be at least 8 characters long, "
                                   "including at least one uppercase letter, "
                                   "one lowercase letter, one digit, and one special character.",
                    }
                ], safe=False)

        if username and email and not raw_password1 and not raw_password2:
            pass

        else:
            if re.match(pattern='^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', string=raw_password1):
                if raw_password2 == raw_password1:
                    new_user = User(username=username, email=email, password=make_password(password=raw_password1))
                    new_user.save()

                    return JsonResponse(data=[
                        {
                            "valid": True,
                            "field": "userName",
                            "message": "The username is valid.",
                        },
                        {
                            "valid": True,
                            "field": "email",
                            "message": "The e-mail address is valid.",
                        },
                        {
                            "valid": True,
                            "field": "password1",
                            "message": "The password is valid.",
                        },
                        {
                            "valid": True,
                            "field": "password2",
                            "message": "The confirm password is valid.",
                        }
                    ], safe=False)

                else:
                    return JsonResponse(data=[
                        {
                            "valid": True,
                            "field": "userName",
                            "message": "The username is valid.",
                        },
                        {
                            "valid": True,
                            "field": "email",
                            "message": "The e-mail address is valid.",
                        },
                        {
                            "valid": True,
                            "field": "password1",
                            "message": "The password is valid.",
                        },
                        {
                            "valid": True,
                            "field": "password2",
                            "message": "The confirm password field does not match the previously entered password.",
                        }
                    ], safe=False)

            else:
                return JsonResponse(data=[
                    {
                        "valid": True,
                        "field": "userName",
                        "message": "The username is valid.",
                    },
                    {
                        "valid": True,
                        "field": "email",
                        "message": "The e-mail address is valid.",
                    },
                    {
                        "valid": True,
                        "field": "password1",
                        "message": "The password should be at least 8 characters long, "
                                   "including at least one uppercase letter, "
                                   "one lowercase letter, one digit, and one special character.",
                    },
                    {
                        "valid": True,
                        "field": "password2",
                        "message": "The confirm password field does not match the previously entered password.",
                    }
                ], safe=False)

    else:
        return JsonResponse(data={
            "data": [
                {
                    "valid": False,
                    "message": "It is not possible to register a new user.",
                }
            ]
        })


def login(request):
    return render(request=request, template_name='accounts/login.html', context={
        'title': 'Login'
    })


def logout(request):
    pass
