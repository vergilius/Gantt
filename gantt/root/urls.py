from django.conf.urls import patterns, include, url
from django.contrib import admin

import gantt.views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'gantt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', gantt.views.home),
    url(r'^login/$', gantt.views.login),
    url(r'^admin/', include(admin.site.urls)),
)
