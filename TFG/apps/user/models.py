__author__ = 'oskyar'

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    dni = models.CharField(max_length=9, blank=True, null=True)
    photo = models.ImageField(upload_to='profiles', blank=True, null=True)

    def __unicode__(self):
        return self.user.username

