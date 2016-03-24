from django.conf import settings
from django.contrib.auth import login, get_backends
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from registration.signals import login_user
from ..user.models import UserProfile
from django.contrib.auth.models import User


@receiver(user_logged_in)
def add_profile_to_session(sender, user, request, **kwargs):
    user_profile = UserProfile.objects.get_user_by_username(user)
    request.session['photo'] = settings.MEDIA_URL + str(user_profile.photo)
    #print(request.session.keys())


@receiver(user_logged_out)
def remove_profile_to_session(sender, user, request, **kwargs):
    del request.session['photo']
