__author__ = 'oskyar'

# accounts/urls.py

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register_user_view, name='account.register'),
    url(r'thanks/(?P<username>[\w]+)/$', views.thanks_view, name='accounts.thanks'),
]
