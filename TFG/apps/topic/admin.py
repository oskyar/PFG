__author__ = 'oskyar'

# user/admin.py

from django.contrib import admin
from .models import Topic, Subtopic

admin.site.register(Topic)
admin.site.register(Subtopic)

