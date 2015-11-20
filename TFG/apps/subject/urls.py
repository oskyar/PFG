__author__ = 'oskyar'

# accounts/urls.py

from django.conf.urls import url

from .views import RegisterUser, ThanksView

urlpatterns = [
    url(r'^register/$', RegisterUser.as_view(), name="register"),
    url(r'thanks/$', ThanksView.as_view(), name="thanks"),

    # url(r'thanks/(?P<username>[\w]+)/$', ThanksView.as_view(), name="thanks"),
]
