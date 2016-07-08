from django.conf.urls import patterns, url
from django.contrib import admin
from .views import Error403, Error404, Error500

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'TFG.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Inicio

    url(r'^403$', Error403.as_view(), name='error403'),
    url(r'^404$', Error404.as_view(), name='error404'),
    url(r'^500$', Error500.as_view(), name='error500'),
]
