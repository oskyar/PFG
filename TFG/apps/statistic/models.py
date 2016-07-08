__author__ = 'oskyar'

from TFG.apps.question.models import Question
from django.db import models

# Asignatura.
class StatisticQuestion(models.Model):
    # id = Id creada por defecto por django
    question = models.OneToOneField('question.Question', related_name='statistic')
    num_generated = models.PositiveIntegerField(default=0)
    num_answered = models.PositiveIntegerField(default=0)
    num_successful = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s (%d-%d-%d)" % (self.question.statement, self.num_generated, self.num_answered, self.num_successful)
