__author__ = 'oskyar'

from django.conf.urls import url, include
from . import views

urlpatterns = [
    # url(r'^(?P<pk>\w+)/doit/', include('TFG.apps.topic.urls')),
    url(r'^create$', views.CreateTestView.as_view(), name='create_test'),
    url(r'^(?P<pk_test>\w+)/delete$', views.DeleteTestView.as_view(), name='delete_test'),
    url(r'^doit$', views.DoTestView.as_view(), name='do_test'),
    url(r'^doingit/(?P<pk_test>\w+)$', views.DoingTestView.as_view(), name='doing_test'),
    url(r'^doingit/(?P<pk_test>\w+)/correct_test$', views.DoneTestView.as_view(), name='correct_test'),
    url(r'^doitanddoingit/(?P<pk_subtopic>\w+)/$', views.DoTestRedirectDoingTest.as_view(), name='doanddoing_test')
    # url(r'^$', views.ListTestView.as_view(), name='list_tests'),
    # url(r'^ajax-upload$', views.import_uploader, name="my_ajax_upload"),
    # url(r'thanks/(?P<username>[\w]+)/$', ThanksView.as_view(), name="thanks"),
]
