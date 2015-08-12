from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import TFG.core.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TFG.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TFG.core.views.index, name='index'),
    url(r'^db', TFG.core.views.db, name='db'),
)
