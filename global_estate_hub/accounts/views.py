from django.shortcuts import render, redirect
from django.http import JsonResponse
import json


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
        password1_field = data['password1'][1]

        password2 = data['password2'][0]
        password2_field = data['password2'][1]

        if username:
            return JsonResponse(data={
                "valid": True,
                "message": "Correct username",
            })

        if email:
            return JsonResponse(data={
                "valid": True,
                "message": "Correct e-mail address."
            })

        if password1:
            return JsonResponse(data={
                "valid": True,
                "message": "Correct password.",
            })

        if password2:
            return JsonResponse(data={
                "valid": True,
                "message": "Password correctly repeated.",
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
