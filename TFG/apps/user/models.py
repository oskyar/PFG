__author__ = 'oskyar'

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from s3direct.fields import S3DirectField


class UserProfileManager(models.Manager):
    def get_user_by_email(self, email):
        # user = User.objects.get(email=email)
        try:
            return self.get(user=User.objects.get(email=email).id)
        except UserProfile.DoesNotExist:
            return None

    def get_user_by_username(self, username):
        try:
            return self.get(user=User.objects.get(username=username).id)
        except UserProfile.DoesNotExist:
            return None

    def num_test_by_user(self, *args, **kwargs):
        return self.sub


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userProfile')
    tests_registered = models.ManyToManyField(
        'test.Test',
        related_name='students', blank=True)

    dni = models.CharField(max_length=9, blank=True, null=True)
    photo = S3DirectField(dest='profiles', blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=False)
    modify_on = models.DateTimeField(blank=True, null=False)
    level = models.PositiveIntegerField(default=0, blank=True, null=False)
    score = models.PositiveIntegerField(default=0, blank=True, null=False)

    objects = UserProfileManager()

    class Meta:
        verbose_name = "Perfil de usuario"

    def set_password(self, raw_password):
        self.user.set_password(raw_password)

    def __str__(self):
        return self.user.get_username()


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dni', 'photo', 'created_on', 'modify_on')


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
