__author__ = 'oskyar'

# user/admin.py

from django.contrib import admin
from .models import Test, TestDone

admin.site.register(Test)
admin.site.register(TestDone)

