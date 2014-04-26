from django.contrib import admin

from domain.models import (
    Team,
    Assignment,
    Project,
    ProjectAssignment,
    Task,
)


class TeamAdmin(admin.ModelAdmin):

    pass


class AssignmentAdmin(admin.ModelAdmin):

    pass


class ProjectAdmin(admin.ModelAdmin):

    pass


class ProjectAssignmentAdmin(admin.ModelAdmin):

    pass


class TaskAdmin(admin.ModelAdmin):

    pass


admin.site.register(Team, TeamAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectAssignment, ProjectAssignmentAdmin)
admin.site.register(Task, TaskAdmin)
