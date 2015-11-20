__author__ = 'oskyar'

from django.db import models
from .admin import UserProfile



# Asignatura
class Subject(models.Model):
    # id = Id creada por defecto por django
    teacher = models.OneToMany(to=UserProfile)
    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.CharField(max_length=512, blank=False, null=False)
    category = models.CharField(max_length=75, blank=False, null=False)
    test_opt = models.BooleanField(default=False, blank=False, null=False)
    capacity = models.IntegerField(max_length=4, null=True)
    image = models.ImageField(upload_to='subject', blank=True, null=True)

    def __unicode__(self):
        return self.name


# Tema
class Topic(models.Model):
    # id = Id creada por defecto por django
    subject = models.ForeignKey(Subject)
    name = models.CharField(max_length=64)
    cardinality = models.IntegerField(max_length=2, blank=False, null=False)
    description = models.CharField(max_length=256)
    value = models.IntegerField(max_length=3, blank=True, null=False)

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
    type = models.IntegerField(max_length=1,
                                      choices=TYPES_CHOICES,
                                      default=STANDARD)

# Respuesta
class Answer(models.Model):
    # id = Id generado por defecto por django
    question = models.ForeignKey(Question)
    statistic = models.OneToOneField(to=StatisticAnswer)
    reply = models.CharField(max_length=300, blank=False, null=False)
    valid = models.BooleanField(default=False, blank=False, null=False)
    adjustment = models.IntegerField(max_length=3, blank=True, null=True)

# Estadísticas pregunta
class StatisticAnswer(models.Model):
    # id = Id generado por defecto por django
    num_generate = models.IntegerField(default=0, null=False, blank=False)
    num_replies = models.IntegerField(default=0, null=False, blank=False)
    num_correct = models.IntegerField(default=0, null=False, blank=False)



admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Answer)
