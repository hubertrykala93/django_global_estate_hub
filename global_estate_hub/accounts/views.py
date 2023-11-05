from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponseRedirect
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

        response = [
            {
                "valid":
                    False if not username else
                    False if not re.match(pattern='^[a-zA-Z0-9_.-]+$', string=username) else
                    False if re.match(pattern='^[a-zA-Z0-9_.-]+$', string=username) and User.objects.filter(
                        username=username).exists() else
                    True,
                "field": "userName",
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
                "field": "email",
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
                "field": "password1",
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
                "field": "password2",
                "message":
                    "The confirm password field cannot be empty." if not raw_password2 else
                    "The password field must be filled in." if not raw_password1 else
                    "The confirm password field does not match the previously entered password." if raw_password2 != raw_password1 else
                    "Correct password confirmation.",
            }
        ]

        if list(set([data['valid'] for data in response]))[0]:
            user = User(username=username, email=email, password=make_password(password=raw_password1))
            user.save()

            return JsonResponse(data=response, safe=False)

        else:
            return JsonResponse(data=response, safe=False)

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
