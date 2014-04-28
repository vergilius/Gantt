from django.conf.urls import patterns, include, url
from django.contrib import admin

import domain.views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'gantt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', domain.views.home),
    url(r'^login/$', domain.views.login),
    url(r'^admin/', include(admin.site.urls)),
)
