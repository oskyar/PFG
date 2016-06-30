__author__ = 'oskyar'

# user/admin.py

from django.contrib import admin
from .models import StatisticQuestion

#from TFG.apps.statistic.models import

admin.site.register(StatisticQuestion)

