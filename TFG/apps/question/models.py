__author__ = 'oskyar'

from django.db import models
from django.utils.translation import ugettext as _
from s3direct.fields import S3DirectField


# Preguntas
class Question(models.Model):
    STANDARD = 0
    MULTIPLE = 1
    TOF = 2
    IMAGE = 3
    TYPES_CHOICES = (
        (STANDARD, _("Una respuesta válida")),
        (MULTIPLE, _("Varias respuestas válidas")),
        #        (TOF, "Verdadero o Falso"),
        # (IMAGE, "El contexto de la pregunta es la imagen"),
    )

    # id = Id generado por defecto por django
    subtopic = models.ForeignKey('topic.Subtopic', related_name='questions', on_delete=models.CASCADE)
    statement = models.CharField(max_length=150)
    image = S3DirectField(dest='questions', blank=True, null=True)
    type = models.IntegerField(choices=TYPES_CHOICES,
                               default=STANDARD)

    class Meta:
        ordering = ['statement']

    def __str__(self):
        return "%s(%s)" % (self.statement, self.subtopic.name)