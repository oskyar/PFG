from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
from django.views.static import serve
import logging
from importlib import import_module
from django.conf import settings

# from TFG.apps.user.forms import UserProfileForm
# from registration.views import RegistrationView

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'TFG.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', login, {'template_name': 'index/index.html'},
        name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),

    url(r'^', include('TFG.apps.index.urls')),
    # url(r'^db', TFG.apps.index.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^user/', include('TFG.apps.user.urls')),
    url(r'^subject/', include('TFG.apps.subject.urls')),
    url(r'^search/',include('TFG.apps.search.urls')),
    # url(r'^test/', include('TFG.apps.test.urls')),

    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT,}),
]

import_module("TFG.apps.index.signals")

# Este código sirve para buscar todos los signals añadidos a las apps
"""logger = logging.getLogger(__name__)

signal_modules = {}

for app in settings.INSTALLED_APPS:
    signals_module = '%s.signals' % app
    try:
        logger.debug('loading "%s" ..' % signals_module)
        signal_modules[app] = import_module(signals_module)
    except ImportError as e:
        logger.warning(
            'failed to import "%s", reason: %s' % (signals_module, str(e)))
"""
