__author__ = 'oskyar'

from TFG.apps.user.models import UserProfile
from django.db import models
from django.utils.translation import ugettext as _


# Asignatura.
class Subject(models.Model):
    # id = Id creada por defecto por django
    teacher = models.ForeignKey(UserProfile, related_name='userProfile')
    name = models.CharField(max_length=128, blank=False, null=False, verbose_name=_("Nombre de la asignatura"))
    description = models.CharField(max_length=512, blank=False, null=False, verbose_name=_("Breve descripción, máximo 512 caracteres"))
    category = models.CharField(max_length=75, blank=False, null=False, verbose_name=_("Categoría"))
    test_opt = models.BooleanField(blank=False, null=False, verbose_name=_("Examen final directo"))
    capacity = models.IntegerField(null=True, verbose_name=_("Nº de alumnos"))
    image = models.ImageField(upload_to='subjects', blank=True, null=True, verbose_name=_("Imagen de la asignatura"))
    #pos_image = models.CharField(blank=True, null=True, max_length=250)

    def __str__(self):
        return self.name + " (" + self.category + ")"


# Tema
class Topic(models.Model):
    subject = models.ForeignKey(Subject, related_name='topics', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    cardinality = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=256)
    value = models.IntegerField(blank=True, null=False)

    def __str__(self):
        return self.name + " (" + self.subject.name + ")"


# Preguntas
class Question(models.Model):
    STANDARD = 0
    MULTIPLE = 1
    TOF = 2
    IMAGE = 3
    TYPES_CHOICES = (
        (STANDARD, "Una respuesta válida"),
        (MULTIPLE, "Varias respuestas válidas"),
        #        (TOF, "Verdadero o Falso"),
        # (IMAGE, "El contexto de la pregunta es la imagen"),
    )

    # id = Id generado por defecto por django
    topic = models.ForeignKey(Topic, related_name='question', on_delete=models.CASCADE)
    statement = models.CharField(max_length=150)
    image = models.ImageField(upload_to='question', blank=True, null=True)
    type = models.IntegerField(choices=TYPES_CHOICES,
                               default=STANDARD)


# Estadísticas pregunta
class StatisticAnswer(models.Model):
    # id = Id generado por defecto por django
    answer = models.OneToOneField('subject.Answer', related_name="statistic")
    num_generate = models.IntegerField(default=0, null=False, blank=False)
    num_replies = models.IntegerField(default=0, null=False, blank=False)
    num_correct = models.IntegerField(default=0, null=False, blank=False)


# Respuestas
class Answer(models.Model):
    # id = Id generado por defecto por django
    question = models.ForeignKey(Question, related_name="answer")
    reply = models.CharField(max_length=300, blank=False, null=False)
    valid = models.BooleanField(default=False, blank=True, null=False)
    adjustment = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return "%s - %s - %s" % (self.question.statement, self.reply, self.valid)

    def __unicode__(self):
        return "%s - %s - %s" % (self.question.statement, self.reply, self.valid)
