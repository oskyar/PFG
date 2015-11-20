from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
from django.views.static import serve

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
    url(r'^user/', include('TFG.apps.user.urls')),
    url(r'^subject/', include('TFG.apps.subject.urls')),

    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT,}),
]
