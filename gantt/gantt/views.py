from django.shortcuts import render, redirect
from django.contrib.auth import logout, forms, authenticate, login


def login_required(func):

    def inner(request):
        if not request.user.is_authenticated():
            return redirect('/login/')
        else:
            return func(request)

    return inner


@login_required
def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        form = forms.AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            login(request, user)
            return redirect('/')
    else:
        form = forms.AuthenticationForm()

    return render(request, 'login.html', {
        'form': form,
    })


def logout_view(request):
    logout(request)
    return redirect('/')
