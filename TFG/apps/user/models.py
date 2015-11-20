__author__ = 'oskyar'

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from registration.models import RegistrationProfile

from django.contrib import admin


class UserProfileManager(models.Manager):
    def get_user_by_email(self, email):
        #user = User.objects.get(email=email)
        try:
            return UserProfile.objects.get(user=User.objects.get(email=email))
        except User.DoesNotExist:
            return None

    def get_user_by_username(self, username):
        return UserProfile.objects.get(user=User.objects.get(username=username))



class UserProfile(models.Model):
    print("Entra en userProfile")
    user = models.OneToOneField(User)
    dni = models.CharField(max_length=9, blank=True, null=True)
    photo = models.ImageField(upload_to='profiles', blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=False)
    modify_on = models.DateTimeField(blank=True, null=False)

    objects = UserProfileManager()

    class Meta:
        verbose_name = "Perfil de usuario"


    def __str__(self):
        return self.user.get_username()


class UserProfileAdmin (admin.ModelAdmin):
    list_display = ('user','dni', 'photo', 'created_on', 'modify_on')


"""
def user_registered_callback(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.name = request.POST["name"]
    profile.surname = request.POST["surname"]
    profile.email = request.POST["email"]
    profile.dni = request.POST["dni"]
    print("ENTra en metodo")
    if 'photo' in request.FILES:
        profile.photo = request.FILES['photo']

    profile.save()


user_registered.connect(user_registered_callback)"""