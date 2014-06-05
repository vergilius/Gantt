from copy import copy
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login, forms as dj_forms
from django.http import Http404

from . import models, forms

DAY_SPAN = 8


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
        form = dj_forms.AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            login(request, user)
            return redirect('/')
    else:
        form = dj_forms.AuthenticationForm()

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


def _day_generator(start):

    start_date = copy(start)

    while True:
        yield start_date.day
        start_date = start_date + timedelta(days=1)

@login_required
def project(request, project):
    project = get_object_or_404(models.Project, pk=project)

    if not project.team in request.user.team_set.all():
        raise Http404()

    if not project in request.user.project_set.all():
        raise Http404()

    project_start, project_end = project.get_span()
    delta = project_end - project_start
    gen = _day_generator(project_start)
    project_span = []
    for i in range(delta.days + 1):
        project_span.append(gen.next())

    graph = []
    for task in project.top_down_tasks():
        graph.append({
            'offset': task.get_offset(project_start),
            'duration': task.get_days_span(),
            'has_subtasks': task.has_subtasks(),
        })

    top_tasks = []
    sub_tasks = {}
    for task in project.top_down_tasks():
        top_id = task.get_top_parent_id()

        if top_id is None:
            top_tasks.append(task)
        else:
            if top_id not in sub_tasks:
                sub_tasks[top_id] = []
            sub_tasks[top_id].append(task)

    top_sub_tasks = []
    for task in top_tasks:
        top_sub_tasks.append({
            'task': task,
            'subtasks': sub_tasks.get(task.id),
        })

    return render(request, 'project.html', {
        'project': project,
        'project_span': project_span,
        'day_span': DAY_SPAN,
        'graph': graph,
        'top_sub_tasks': top_sub_tasks,
    })

@login_required
def new_task(request, project):
    project = get_object_or_404(models.Project, pk=project)

    if not project.team in request.user.team_set.all():
        raise Http404()

    if not project in request.user.project_set.all():
        raise Http404()

    if request.method == 'POST':
        task_form = forms.TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project', project=task.project.pk)
    else:
        task_form = forms.TaskForm()

    return render(request, 'new.html', {
        'task_form': task_form,
    })

@login_required
def edit_task(request, project, task):
    project = get_object_or_404(models.Project, pk=project)
    task = get_object_or_404(models.Task, pk=task)

    if not project.team in request.user.team_set.all():
        raise Http404()

    if not project in request.user.project_set.all():
        raise Http404()

    if request.method == 'POST':
        task_form = forms.TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            return redirect('project', project=task.project.pk)
    else:
        task_form = forms.TaskForm(instance=task)

    return render(request, 'edit.html', {
        'task_form': task_form,
        'task': task,
    })
