__author__ = 'oskyar'

from django.db import models
from django.utils.translation import ugettext as _
from s3direct.fields import S3DirectField
from smart_selects.db_fields import ChainedManyToManyField


# Manager de Asignatura
class SubjectManager(models.Manager):
    def owner(self, pk_subject):
        return self.get(pk=pk_subject).teacher

    def by_owner(self, userProfile):
        return self.filter(teacher=userProfile)

    def get_num_questions(self, subject, type=None):
        num_questions = 0
        for topic in subject.topics.all():
            if type:
                for subtopic in topic.subtopics.all():
                    num_questions += subtopic.questions.filter(type=type).count()
            else:
                for subtopic in topic.subtopics.all():
                    num_questions += subtopic.questions.all().count()

        return num_questions

    def get_all_questions(self, subject, type=None):
        questions = list()
        for topic in subject.topics.all():
            if type:
                for subtopic in topic.subtopics.all():
                    questions += subtopic.questions.filter(type=type)
            else:
                for subtopic in topic.subtopics.all():
                    questions += subtopic.questions.all()

        return questions


# Asignatura.
class Subject(models.Model):
    # id = Id creada por defecto por django
    teacher = models.ForeignKey(
        'user.UserProfile',
        related_name='subjects')
    students = ChainedManyToManyField(
        'user.UserProfile',
        chained_field='student',
        chained_model_field='user',
        auto_choose=True,
        related_name="my_subjects")
    name = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        verbose_name=_("Nombre de la asignatura"))
    description = models.CharField(
        max_length=512,
        blank=False,
        null=False,
        verbose_name=_("Breve descripción, máximo 512 caracteres"))
    category = models.CharField(
        max_length=75,
        blank=False,
        null=False,
        verbose_name=_("Categoría"))
    test_opt = models.BooleanField(
        blank=False,
        null=False,
        verbose_name=_("Examen final directo"))
    capacity = models.IntegerField(
        null=True,
        verbose_name=_("Nº máx. alumnos"))
    image = S3DirectField(
        dest='subjects',
        blank=True,
        null=True,
        verbose_name="Imagen de la asignatura")
    created_on = models.DateTimeField(blank=True, null=False)
    # pos_image = models.CharField(blank=True, null=True, max_length=250)

    objects = SubjectManager()

    class Meta:
        permissions = (
            ('view_subject', 'View detail Subject'),
            ('register_subject', 'Student registers of subject'),
            ('unregister_subject', 'Student unregisters of subject')
        )

    def __str__(self):
        return self.name + " (" + self.category + ")"
