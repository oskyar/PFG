__author__ = 'oskyar'

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^(?P<search>[\w ]+)$', views.SearchView.as_view(), name='search'),
]
