from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

import TFG.apps.index.views
import TFG.apps.user.views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'TFG.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^$', include('TFG.apps.index.urls')),
                       # url(r'^db', TFG.apps.index.views.db, name='db'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^user/', include('TFG.apps.user.urls')),

                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT, }),
                       )
