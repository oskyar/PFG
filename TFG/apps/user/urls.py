__author__ = 'oskyar'

# accounts/urls.py

from django.conf.urls import url, include
from .views import UserProfileView, UserProfileUpdateView, ClasificationSubject

urlpatterns = [
    url(r'^register/$', UserProfileView.as_view(), name='registration_register'),

    url(r'^edit/(?P<pk>\w+)/$', UserProfileUpdateView.as_view(), name='edit_profile'),
    url(r'^clasification/$', ClasificationSubject.as_view(), name='clasification_user'),
    #url(r'register/$', RegisterUser.as_view(), name="register_user"),
    url(r'^', include('registration.backends.default.urls')),
    #url(r'thanks/$', ThanksView.as_view(), name="thanks"),

    # url(r'thanks/(?P<username>[\w]+)/$', ThanksView.as_view(), name="thanks"),
]
