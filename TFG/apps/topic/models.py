__author__ = 'oskyar'

from TFG.apps.subject.models import Subject
from django.db import models


class TopicManager(models.Manager):
    def gamificado(self):
        return self.filter(gamificar=True)


# Tema
class Topic(models.Model):
    subject = models.ForeignKey(Subject, related_name='topics', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    cardinality = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=256)
    value = models.IntegerField(blank=True, null=False)
    gamificar = models.BooleanField(blank=False, null=False, default=True)

    objects = TopicManager()

    class Meta:
        ordering = ['cardinality', 'name']

    def __str__(self):
        return self.name + " (" + self.subject.name + ")"


class SubtopicManager(models.Manager):
    def gamificado(self):
        return self.filter(gamificar__exact=True)


class Subtopic(models.Model):
    topic = models.ForeignKey(Topic, related_name='subtopics', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    cardinality = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=256)
    value = models.IntegerField(blank=True, null=False)
    gamificar = models.BooleanField(blank=False, null=False, default=True)

    objects = SubtopicManager()

    class Meta:
        ordering = ['cardinality']

    def __str__(self):
        return self.name + " (" + self.topic.name + ")"
