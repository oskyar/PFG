__author__ = 'oskyar'


# accounts/admin.py

from django.contrib import admin

from .models import UserProfile

admin.site.register(UserProfile)