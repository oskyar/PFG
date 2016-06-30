__author__ = 'oskyar'

from django.conf.urls import url, include
from . import views

urlpatterns = [
    #url(r'^(?P<pk>\w+)/doit/', include('TFG.apps.topic.urls')),
    url(r'^create$', views.CreateTestView.as_view(), name='create_test'),
    #url(r'^$', views.ListTestView.as_view(), name='list_tests'),
    #url(r'^ajax-upload$', views.import_uploader, name="my_ajax_upload"),
    # url(r'thanks/(?P<username>[\w]+)/$', ThanksView.as_view(), name="thanks"),
]
