from django.shortcuts import render


def sign_up(request):
    return render(request=request, template_name='accounts/sign-up.html', context={
        'title': 'Sign Up',
    })
