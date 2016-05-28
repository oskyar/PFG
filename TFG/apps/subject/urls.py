__author__ = 'oskyar'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<pk_subject>\d+)/topic/(?P<pk_topic>\d+)/question/create', views.CreateQuestionView.as_view(),
        name='create_question'),
    url(r'^(?P<pk_subject>\d+)/topic/(?P<pk_topic>\d+)/question/delete/(?P<pk_question>\d+)',
        views.DeleteQuestionView.as_view(), name='delete_question'),
    # url(r'^(?P<pk>\w+)/topic/?P<pk_topic>/', DetailTopicView.as_view(), name='create_topic'),
    url(r'^(?P<pk>\w+)/topic/create$', views.CreateTopicView.as_view(), name='create_topic'),
    url(r'^list', views.ListSubjectView.as_view(), name='list_subjects'),
    url(r'^create$', views.CreateSubjectView.as_view(), name='create_subject'),
    url(r'^start$', views.start, name="start"),
    url(r'^ajax-upload$', views.import_uploader, name="my_ajax_upload"),
    # url(r'thanks/(?P<username>[\w]+)/$', ThanksView.as_view(), name="thanks"),
]
