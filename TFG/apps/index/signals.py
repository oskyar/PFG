from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


@receiver(user_logged_in)
def add_profile_to_session(sender, user, request, **kwargs):
    # user_profile = UserProfile.objects.get_user_by_username(user)
    try:
        if user.userProfile.photo is not None:
            request.session['photo'] = userProfile.photo.url
    except:
        print("No existe foto")


@receiver(user_logged_out)
def remove_profile_to_session(sender, user, request, **kwargs):
    try:
        del request.session['photo']
    except:
        print("No existe foto")
