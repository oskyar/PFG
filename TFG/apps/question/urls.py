__author__ = 'oskyar'

from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^list', views.ListSubjectView.as_view(), name='list_subjects'),
    url(r'^create$', views.CreateQuestionView.as_view(), name='create_question'),
    url(r'^(?P<pk_question>\d+)/delete$', views.DeleteQuestionView.as_view(), name='delete_question'),
]
