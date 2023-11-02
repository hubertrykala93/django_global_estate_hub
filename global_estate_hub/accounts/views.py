from django.shortcuts import render


def register(request):
    return render(request=request, template_name='accounts/register.html', context={
        'title': 'Sign Up',
    })


def login(request):
    return render(request=request, template_name='accounts/login.html', context={
        'title': 'Login'
    })


def logout(request):
    pass
