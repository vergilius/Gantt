from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, forms, authenticate, login
from django.http import Http404

from . import models


def login_required(func):

    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/login/')
        else:
            return func(request, *args, **kwargs)

    return inner


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


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def team(request, team):
    try:
        team = models.Team.objects.get(name=team)
    except models.Team.DoesNotExist:
        raise Http404()

    if not team in request.user.team_set.all():
        raise Http404()

    return render(request, 'team.html', {
        'team': team,
        'projects': team.get_projects_for(request.user),
    })


@login_required
def project(request, project):
    try:
        project = models.Project.objects.get(pk=project)
    except models.Project.DoesNotExist:
        raise Http404()

    if not project.team in request.user.team_set.all():
        raise Http404()

    if not project in request.user.project_set.all():
        raise Http404()

    return render(request, 'project.html', {
        'project': project,
    })
