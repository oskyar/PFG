from django.dispatch import Signal
from django.dispatch import receiver

"""
update_user_profile = Signal(providing_args=['userProfile', 'request'])


@receiver(update_user_profile)
def change_photo_user(sender, user, request, **kwargs):
    try:
        if user.photo is not None:
            request.session['photo'] = user.photo.url
    except:
        print("No existe foto")


update_user_profile.connect(change_photo_user)
"""

