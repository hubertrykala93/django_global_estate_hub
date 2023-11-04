from django.shortcuts import render, redirect
from django.http import JsonResponse


def register(request):
    return render(request=request, template_name='accounts/register.html', context={
        'title': 'Sign Up',
    })


def create_user(request):
    if request.method == 'POST':
        post_data = request.POST
        body_data = request.body

        print(post_data)
        print(body_data)

        return redirect(to='index')


def login(request):
    return render(request=request, template_name='accounts/login.html', context={
        'title': 'Login'
    })


def logout(request):
    pass
