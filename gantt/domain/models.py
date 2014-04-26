from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):

    name = models.CharField(max_length=255, primary_key=True, blank=False)
    users = models.ManyToManyField(User, through='Assignment')

    def __unicode__(self):
        return self.name


class Assignment(models.Model):

    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    role = models.CharField(max_length=255, blank=False)

    class Meta:

        unique_together = ('user', 'team')


class Project(models.Model):

    team = models.ForeignKey(Team)
    name = models.CharField(max_length=255, blank=False)
    users = models.ManyToManyField(User, through='ProjectAssignment')


class ProjectAssignment(models.Model):

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    role = models.CharField(max_length=255)

    class Meta:

        unique_together = ('user', 'project')


class Task(models.Model):

    project = models.ForeignKey(Project)
    developer = models.ForeignKey(User)
    parent_task = models.ForeignKey('self')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    priority = models.IntegerField()
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=255)
    realization = models.IntegerField()
