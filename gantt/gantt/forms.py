from django import forms

from . import models


class TaskForm(forms.ModelForm):

    class Meta(object):

        model = models.Task
        fields = [
            'developer', 'parent_task', 'name', 'description', 'priority',
            'start_date', 'due_date', 'status', 'realization',
        ]
