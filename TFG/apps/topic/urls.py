__author__ = 'oskyar'

from django.conf.urls import url, include
from . import views
from . import models

urlpatterns = [
    url(r'^(?P<pk_topic>\d+)/subtopic/(?P<pk_subtopic>\d+)/question/', include('TFG.apps.question.urls')),
    url(r'^(?P<pk_topic>\d+)/subtopic/create$', views.CreateSubtopicView.as_view(), name='create_subtopic'),
    url(r'^(?P<pk_topic>\d+)/subtopic/$', views.ListSubtopicView.as_view(), name='list_subtopic'),
    url(r'^(?P<pk_topic>\d+)/subtopic/(?P<pk_subtopic>\d+)$', views.DetailSubtopicView.as_view(),
        name='detail_subtopic'),
    url(r'^(?P<pk_topic>\d+)/subtopic/(?P<pk_subtopic>\d+)/edit', views.UpdateSubtopicView.as_view(),
        name="edit_subtopic"),
    url(r'^(?P<pk_topic>\d+)/subtopic/(?P<pk_subtopic>\d+)/delete$', views.DeleteSubtopicView.as_view(),
        name="delete_subtopic"),
    # url(r'^(?P<pk>\w+)/topic/?P<pk_topic>/', DetailTopicView.as_view(), name='create_topic'),
    # url(r'^list', views.ListSubjectView.as_view(), name='list_subjects'),
    url(r'^$', views.ListTopicView.as_view(), name='list_topic'),
    url(r'^(?P<pk_topic>\d+)$', views.DetailTopicView.as_view(), name='detail_topic'),
    url(r'^create$', views.CreateTopicView.as_view(), name='create_topic'),
    url(r'^(?P<pk_topic>\d+)/edit', views.UpdateTopicView.as_view(), name='edit_topic'),
    url(r'^(?P<pk_topic>\d+)/delete$', views.DeleteTopicView.as_view(), name='delete_topic'),
]
