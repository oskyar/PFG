__author__ = 'oskyar'

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from smart_selects.db_fields import ChainedForeignKey
from TFG.apps.question.models import Question


class TestManager(models.Manager):
    def gamificado(self):
        return self.filter(gamificado=True)

    def without_gamificar_by_owner(self, subject, owner):
        return self.filter(owner=owner, gamificado=False, subject=subject)

    def gamificado_by_owner(self, subject, owner):
        return self.filter(owner=owner, gamificado=True, subject=subject)


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
        show_all=True,
        auto_choose=False,
        related_name="tests",
        null=False,
        blank=False,
        verbose_name=_("Asignatura"))
    topic = ChainedForeignKey(
        'topic.Topic',
        chained_field='subject',
        chained_model_field='subject',
        show_all=False,
        auto_choose=False,
        related_name="tests",
        null=True,
        blank=True,
        verbose_name=_("Tema (opcional)"))
    subtopic = ChainedForeignKey(
        'topic.Subtopic',
        chained_field='topic',
        chained_model_field='topic',
        show_all=False,
        auto_choose=False,
        related_name="tests",
        null=True,
        blank=True,
        verbose_name=_("Subtema (opcional)"))
    question = models.ManyToManyField('question.Question', related_name='tests', blank=False)

    # question = models.ManyToManyField(Question, related_name="questions", null=False, blank=False)
    name = models.CharField(max_length=200, blank=True, null=False)
    type = models.IntegerField(choices=TYPES_CHOICES,
                               default=STANDARD)
    type_question = models.IntegerField(choices=Question.TYPES_CHOICES,
                                        default=Question.STANDARD)
    num_question = models.PositiveIntegerField(default=1, null=False, blank=False)
    duration = models.PositiveIntegerField(null=True, blank=True)  # Duración de las preguntas/test
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)  # Fecha límite para hacer el test
    activation_code = models.CharField(max_length=6, null=True, blank=True)  # Activación del test
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    active = models.BooleanField(default=False, null=False, blank=False)
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES, default=PUBLIC)
    created_on = models.DateTimeField(blank=True, null=False)
    gamificado = models.BooleanField(default=False, null=False, blank=True)
    autogenerate_questions = models.BooleanField(default=True, null=False, blank=True)
    objects = TestManager()

    def __str__(self):
        return "%s (%s)" % (self.name, self.owner.user.username)


class TestDoneManager(models.Manager):
    def test_gamificados(self, subject):
        return self.filter(test__gamificado=True, test__subject=subject)

    def has_been_passed(self):
        return self.filter(passed=True)

class TestDone(models.Model):
    student = models.ForeignKey(
        'user.UserProfile',
        related_name="testsdone")
    test = models.ForeignKey(
        'test.Test',
        related_name="testsdone")
    realization_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    presented = models.DateTimeField(null=True, blank=True)
    passed = models.BooleanField(default=False, null=False, blank=False)
    IP = models.GenericIPAddressField(null=True, blank=False)
    result = models.IntegerField(default=0, null=False, blank=False)
    replies = models.TextField(null=True, blank=True)
    score_won = models.IntegerField(null=True, blank=True)
    percent = models.FloatField(null=True, blank=True)

    objects = TestDoneManager()

    def __str__(self):
        return "%d.%s (%s) %s" % (self.id, self.test.name, self.student.user.first_name, self.passed)
