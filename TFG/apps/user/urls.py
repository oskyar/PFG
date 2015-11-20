__author__ = 'oskyar'

# accounts/urls.py

from django.conf.urls import url, include
from .forms import UserProfileForm
from registration.forms import RegistrationForm
from .views import UserProfileView
from registration.views import RegistrationView


urlpatterns = [
    url(r'^register/$', UserProfileView.as_view(), name='registration_register'),
    #url(r'register/$', RegisterUser.as_view(), name="register_user"),
    url(r'^', include('registration.backends.default.urls')),
    #url(r'thanks/$', ThanksView.as_view(), name="thanks"),

    # url(r'thanks/(?P<username>[\w]+)/$', ThanksView.as_view(), name="thanks"),
]
