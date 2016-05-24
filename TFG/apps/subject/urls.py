__author__ = 'oskyar'

from django.conf.urls import url
from .views import CreateSubjectView, CreateTopicView, CreateQuestionView, ListSubjectView, start, import_uploader

urlpatterns = [
    url(r'^(?P<pk_subject>\w+)/topic/(?P<pk_topic>\w+)/question/create', CreateQuestionView.as_view(),
        name='create_question'),
    # url(r'^(?P<pk>\w+)/topic/?P<pk_topic>/', DetailTopicView.as_view(), name='create_topic'),
    url(r'^(?P<pk>\w+)/topic/create$', CreateTopicView.as_view(), name='create_topic'),
    url(r'^list$', ListSubjectView.as_view(), name="list_subjects"),
    url(r'^create$', CreateSubjectView.as_view(), name="create_subject"),
    url(r'^start$', start, name="start"),
    url(r'^ajax-upload$', import_uploader, name="my_ajax_upload")
    # url(r'thanks/(?P<username>[\w]+)/$', ThanksView.as_view(), name="thanks"),
]
