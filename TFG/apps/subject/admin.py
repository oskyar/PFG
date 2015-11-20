__author__ = 'oskyar'

# user/admin.py

from django.contrib import admin
from .models import Answer, Subject, Topic, StatisticAnswer, Question

admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(StatisticAnswer)
admin.site.register(Answer)
