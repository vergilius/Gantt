from django.shortcuts import render, redirect


def login_required(func):

    def inner(request):
        if not request.user.is_authenticated():
            return redirect('/login?next={}'.format(request.path))
        else:
            return func(request)

    return inner


@login_required
def home(request):
    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html')
