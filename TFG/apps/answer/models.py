__author__ = 'oskyar'

from TFG.apps.question.models import Question
from django.db import models


# Respuestas
class Answer(models.Model):
    # id = Id generado por defecto por django
    question = models.ForeignKey(Question, related_name="answer", on_delete=models.CASCADE)
    reply = models.CharField(max_length=300, blank=False, null=False)
    valid = models.BooleanField(default=False, blank=True, null=False)
    adjustment = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        ordering = ['reply']

    def __str__(self):
        return "%s - %s - %s" % (self.question.statement, self.reply, self.valid)

    def __unicode__(self):
        return "%s - %s - %s" % (self.question.statement, self.reply, self.valid)
