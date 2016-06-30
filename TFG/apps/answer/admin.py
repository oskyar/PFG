__author__ = 'oskyar'

# user/admin.py

from django.contrib import admin
from .models import Answer

admin.site.register(Answer)
