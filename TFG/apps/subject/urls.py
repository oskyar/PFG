__author__ = 'oskyar'

from django.conf.urls import url
from .views import CreateSubjectView, start, import_uploader

urlpatterns = [
    url(r'^create$', CreateSubjectView.as_view(), name="create_subject"),
    url(r'^start$', start, name="start"),
    url(r'^ajax-upload$', import_uploader, name="my_ajax_upload")
    # url(r'thanks/(?P<username>[\w]+)/$', ThanksView.as_view(), name="thanks"),
]
