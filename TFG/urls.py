from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import TFG.core.views
import TFG.accounts.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TFG.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('TFG.core.urls')),
    url(r'^db', TFG.core.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('TFG.accounts.urls')),

)
