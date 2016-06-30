__author__ = 'oskyar'

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from smart_selects.db_fields import ChainedForeignKey


# Asignatura.
class Test(models.Model):
    STANDARD = 0  # NORMAL TEST
    CHRONO_TEST = 1  # TIME LIMIT FOR TEST
    CHRONO_QUESTION = 2  # TIME LIMIT FOR QUESTION
    # UNIQUE_QUESTION = 3 #ONLY ONE QUESTION
    # HIDE_VALIDS = 4 #WON'T SHOW CORRECTION TEST, ONLY NUM WRONGS.
    TYPES_CHOICES = (
        (STANDARD, _("Test normal")),
        (CHRONO_TEST, _("Test con cronómetro global")),
        (CHRONO_QUESTION, _("Test con tiempo por pregunta")),
    )

    PUBLIC = 0
    REGISTERED = 1
    PRIVATE = 2
    OWNER = 3
    VISIBILITY_CHOICES = ((PUBLIC, _("Público")),
                          (REGISTERED, _("Usuarios matriculados")),
                          (PRIVATE, _("Usuarios con invitación")),
                          (OWNER, _("Solo visible para el propietario")))

    # id = Id creada por defecto por django
    owner = models.ForeignKey(
        'user.UserProfile',
        related_name="tests")
    subject = ChainedForeignKey(
        'subject.Subject',
        chained_field='owner',
        chained_model_field='teacher',
        show_all=False,
        auto_choose=True,
        related_name="tests",
        null=False,
        blank=True)
    topic = ChainedForeignKey(
        'topic.Topic',
        chained_field='subject',
        chained_model_field='subject',
        show_all=False,
        auto_choose=True,
        related_name="tests",
        null=False,
        blank=False)
    subtopic = ChainedForeignKey(
        'topic.Subtopic',
        chained_field='topic',
        chained_model_field='topic',
        show_all=False,
        auto_choose=True,
        related_name="tests",
        null=False,
        blank=False)
    # question = models.ManyToManyField(Question, related_name="questions", null=False, blank=False)
    name = models.CharField(max_length=200, blank=True, null=False)
    type = models.IntegerField(choices=TYPES_CHOICES,
                               default=STANDARD)
    num_question = models.PositiveIntegerField(default=1, null=False, blank=False)
    duration = models.PositiveIntegerField(null=True, blank=True)  # Duración de las preguntas/test
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)  # Fecha límite para hacer el test
    activation_code = models.CharField(max_length=6, null=True, blank=True)  # Activación del test
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    active = models.BooleanField(default=False, null=False, blank=False)
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES, default=PUBLIC)
    created_on = models.DateTimeField(blank=True, null=False, auto_created=timezone.now())

    def __str__(self):
        return "%s (%s)" % (self.name, self.owner.user.username)
