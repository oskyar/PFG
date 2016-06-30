__author__ = 'oskyar'

# user/admin.py

from django.contrib import admin
from .models import UserProfile, UserProfileAdmin

admin.site.register(UserProfile, UserProfileAdmin)
