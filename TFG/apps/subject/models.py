__author__ = 'oskyar'

from django.db import models
from django.utils.translation import ugettext as _
from smart_selects.db_fields import ChainedManyToManyField
from django.utils import timezone


# Manager de Asignatura
class SubjectManager(models.Manager):
    def owner(self, pk_subject):
        return self.get(pk=pk_subject).teacher

    def by_owner(self, userProfile):
        return self.filter(teacher=userProfile)


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
    image = models.ImageField(
        upload_to='subjects',
        blank=True,
        null=True,
        verbose_name=_("Imagen de la asignatura"))
    created_on = models.DateTimeField(blank=True, null=False, auto_created=timezone.now())
    # pos_image = models.CharField(blank=True, null=True, max_length=250)

    objects = SubjectManager()

    def __str__(self):
        return self.name + " (" + self.category + ")"
