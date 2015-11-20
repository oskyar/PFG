__author__ = 'oskyar'

from django.contrib.auth.models import User
from registration.models import RegistrationProfile
from TFG.apps.user.models import UserProfile
from django.db import models
from django.utils.translation import ugettext as _


# Asignatura.
class Subject(models.Model):
    # id = Id creada por defecto por django
    teacher = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=128, blank=False, null=False, verbose_name=_("Nombre de la asignatura"))
    description = models.CharField(max_length=512, blank=False, null=False, verbose_name=_("Breve descripción, máximo 512 caracteres"))
    category = models.CharField(max_length=75, blank=False, null=False, verbose_name=_("Categoría"))
    test_opt = models.BooleanField(blank=False, null=False, verbose_name=_("Examen final directo"))
    capacity = models.IntegerField(null=True, verbose_name=_("Nº de alumnos"))
    image = models.ImageField(upload_to='subject', blank=True, null=True, verbose_name=_("Imagen de la asignatura"))
    #pos_image = models.CharField(blank=True, null=True, max_length=250)

    def __str__(self):
        return self.name + " (" + self.category + ")"


# Tema
class Topic(models.Model):
    # id = Id creada por defecto por django
    subject = models.ForeignKey(Subject)
    name = models.CharField(max_length=64)
    cardinality = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=256)
    value = models.IntegerField(blank=True, null=False)


# Preguntas
class Question(models.Model):
    STANDARD = 0
    TOF = 1
    MULTIPLE = 2
    IMAGE = 3
    TYPES_CHOICES = (
        (STANDARD, 'Una respuesta válida'),
        (TOF, 'Verdadero o Falso'),
        (MULTIPLE, 'Varias respuestas válidas'),
        (IMAGE, 'El contexto de la pregunta es la imagen'),
    )

    # id = Id generado por defecto por django
    topic = models.ForeignKey(Topic)
    statement = models.CharField(max_length=150)
    image = models.ImageField(upload_to='question', blank=True, null=True)
    type = models.IntegerField(choices=TYPES_CHOICES,
                               default=STANDARD)


# Estadísticas pregunta
class StatisticAnswer(models.Model):
    # id = Id generado por defecto por django
    num_generate = models.IntegerField(default=0, null=False, blank=False)
    num_replies = models.IntegerField(default=0, null=False, blank=False)
    num_correct = models.IntegerField(default=0, null=False, blank=False)


# Respuesta
class Answer(models.Model):
    # id = Id generado por defecto por django
    question = models.ForeignKey(Question)
    statistic = models.OneToOneField(to=StatisticAnswer)
    reply = models.CharField(max_length=300, blank=False, null=False)
    valid = models.BooleanField(default=False, blank=False, null=False)
    adjustment = models.IntegerField(blank=True, null=True)

