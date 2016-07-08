__author__ = 'oskyar'

from TFG.apps.subject.models import Subject
from django.db import models
from TFG.apps.question.models import Question


class TopicManager(models.Manager):
    def gamificado(self):
        return self.filter(gamificar=True)

    def get_num_questions(self, topic, type=None):
        num_questions = 0
        if type:
            for subtopic in topic.subtopics.all():
                num_questions += subtopic.questions.filter(type=type).count()
        else:
            for subtopic in topic.subtopics.all():
                num_questions += subtopic.questions.all().count()

        return num_questions

    def get_all_questions(self, topic, type=None):
        questions = list()
        if type:
            for subtopic in topic.subtopics.all():
                questions += subtopic.questions.filter(type=type)
        else:
            for subtopic in topic.subtopics.all():
                questions += subtopic.questions.all()
        return questions


# Tema
class Topic(models.Model):
    subject = models.ForeignKey(Subject, related_name='topics', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    cardinality = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=512)
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

    def test_done_by_user(self, user):
        return self.filter(topic__subject__teacher__)

    def get_num_questions(self, subtopic, type=None):
        num_questions = 0

        if type:
            num_questions += subtopic.questions.filter(type=type).count()
        else:
            num_questions += subtopic.questions.all().count()

        return num_questions

    def get_all_questions(self, subtopic, type=None):
        questions = list()

        if type is not None:
            questions += subtopic.questions.filter(type=type)
        else:
            questions += subtopic.questions.all()

        return questions

    def has_been_pass(self):
        self.filter(tests)


class Subtopic(models.Model):
    topic = models.ForeignKey(Topic, related_name='subtopics', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    cardinality = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=512)
    value = models.IntegerField(blank=True, null=False)
    gamificar = models.BooleanField(blank=False, null=False, default=True)
    num_questions_gami = models.IntegerField(blank=False, null=False)
    objects = SubtopicManager()

    class Meta:
        ordering = ['cardinality']

    def __str__(self):
        return self.name + " (" + self.topic.name + ")"
