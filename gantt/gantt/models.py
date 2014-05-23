from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):

    name = models.CharField(max_length=255, primary_key=True, blank=False)
    users = models.ManyToManyField(User, through='Assignment')

    def __unicode__(self):
        return self.name

    def get_projects_for(self, user):
        return [
            project for project
            in self.project_set.all()
            if user in project.users.all()
        ]


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

    def top_down_tasks(self):
        for task in self.task_set.filter(
                parent_task__isnull=True).order_by('start_date', 'pk'):
            yield task

            for tt in task.get_subtasks():
                yield tt

    def top_tasks(self):
        return self.task_set.filter(parent_task__isnull=True)

    def get_span(self):
        start_date = min(task.start_date for task in self.top_tasks())
        due_date = max(task.due_date for task in self.top_tasks())
        return start_date, due_date


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
    description = models.CharField(max_length=255, blank=True)
    priority = models.IntegerField(default=0)
    _start_date = models.DateField(name='start_date')
    _due_date = models.DateField(name='due_date')
    status = models.CharField(max_length=255, blank=True)
    realization = models.IntegerField(default=0)

    @property
    def start_date(self):
        if self.task_set.count() > 0:
            return min(task.start_date for task in self.task_set.all())
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @start_date.deleter
    def start_date(self):
        self._start_date = None

    @property
    def due_date(self):
        if self.task_set.count() > 0:
            return max(task.due_date for task in self.task_set.all())
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        self._due_date = value

    @due_date.deleter
    def due_date(self):
        self._due_date = None

    def has_subtasks(self):
        return bool(self.task_set.count())

    def __unicode__(self):
        return '<Task #{} - {}>'.format(self.pk, self.name)

    def get_subtasks(self):
        for sub in self.task_set.order_by('start_date', 'pk'):
            yield sub

            for tt in sub.get_subtasks():
                yield tt

    def save(self, *args, **kwargs):
        if self.start_date > self.due_date:
            raise RuntimeError(
                'Start date must be earlier or the same as due date.')
        super(Task, self).save(*args, **kwargs)

    def get_top_parent_id(self):
        if not self.parent_task:
            return None
        else:
            return self.parent_task.get_top_parent_id() or self.parent_task.id

    def get_offset(self, from_date):
        delta = self.start_date - from_date
        return delta.days

    def get_days_span(self):
        delta = self.due_date - self.start_date
        return delta.days + 1
