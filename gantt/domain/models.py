from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):

    name = models.CharField(max_length=255, primary_key=True, blank=False)
    users = models.ManyToManyField(User, through='Assignment')

    def __unicode__(self):
        return self.name


class Assignment(models.Model):

    TEAM_MANAGER = 'team_manager'
    TEAM_LEADER = 'team_leader'
    TEAM_MEMBER = 'team_member'

    ROLES = [(role, role) for role in [TEAM_MANAGER, TEAM_LEADER, TEAM_MEMBER]]

    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    role = models.CharField(max_length=255, blank=False, choices=ROLES)

    def __unicode__(self):
        return "{} to {} as {}".format(self.user, self.team, self.role)

    class Meta:

        unique_together = ('user', 'team')


class Project(models.Model):

    team = models.ForeignKey(Team)
    name = models.CharField(max_length=255, blank=False)
    users = models.ManyToManyField(User, through='ProjectAssignment')

    def __unicode__(self):
        return self.name


class ProjectAssignment(models.Model):

    PROJECT_MANAGER = 'project_manager'
    PROJECT_MEMBER = 'project_member'

    ROLES = [(role, role) for role in [PROJECT_MANAGER, PROJECT_MEMBER]]

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    role = models.CharField(max_length=255, blank=False, choices=ROLES)

    class Meta:

        unique_together = ('user', 'project')


class Task(models.Model):

    project = models.ForeignKey(Project)
    developer = models.ForeignKey(User, blank=True, null=True)
    parent_task = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255)
    priority = models.IntegerField()
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=255)
    realization = models.IntegerField()
