__author__ = 'oskyar'

from django.conf.urls import url, include
from . import views

urlpatterns = [
    # url(r'^(?P<pk>\w+)/topic/?P<pk_topic>/', DetailTopicView.as_view(), name='create_topic'),
    # url(r'^(?P<pk>\w+)/topic/create$', views.CreateTopicView.as_view(), name='create_topic'),
    url(r'^(?P<pk>\w+)/topic/', include('TFG.apps.topic.urls')),
    url(r'^(?P<pk>\w+)/test/', include('TFG.apps.test.urls')),
    url(r'^$', views.ListSubjectView.as_view(), name='list_subjects'),
    url(r'^create$', views.CreateSubjectView.as_view(), name='create_subject'),
    url(r'^(?P<pk>\w+)/unregisterme$', views.UserUnregisterSubject.as_view(), name='unregister_subject'),
    url(r'^(?P<pk>\w+)/registerme$', views.UserRegisterSubject.as_view(), name='register_subject'),
    url(r'^(?P<pk>\w+)/delete$', views.DeleteSubjectView.as_view(), name='delete_subject'),
    url(r'^(?P<pk>\w+)/edit$', views.UpdateSubjectView.as_view(), name='edit_subject'),
    url(r'^(?P<pk>\w+)$', views.DetailSubjectView.as_view(), name='detail_subject'),
    # url(r'thanks/(?P<username>[\w]+)/$', ThanksView.as_view(), name="thanks"),
]
