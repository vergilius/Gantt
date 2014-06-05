from django.conf.urls import patterns, include, url
from django.contrib import admin

import gantt.views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', gantt.views.home),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', gantt.views.login_view),
    url(r'^logout/$', gantt.views.logout_view),
    url(r'^team/(?P<team>\w+)/', gantt.views.team, name="team"),
    url(r'^project/(?P<project>\d+)/$', gantt.views.project, name="project"),
    url(r'^project/(?P<project>\d+)/new/', gantt.views.new_task, name="new_task"),
    url(r'^project/(?P<project>\d+)/edit/(?P<task>\d+)/', gantt.views.edit_task, name="edit_task"),
)
