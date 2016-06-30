__author__ = 'oskyar'

from django.db import models
from django.utils.translation import ugettext as _
from TFG.apps.topic.models import Subtopic
from TFG.apps.test.models import Test


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
    test = models.ManyToManyField(Test, related_name='questions', blank=False)
    subtopic = models.ForeignKey(Subtopic, related_name='questions', on_delete=models.CASCADE)
    statement = models.CharField(max_length=150)
    image = models.ImageField(upload_to='subtopic', blank=True, null=True)
    type = models.IntegerField(choices=TYPES_CHOICES,
                               default=STANDARD)

    class Meta:
        ordering = ['statement']

