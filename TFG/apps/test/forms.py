__author__ = 'oskyar'

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Test
from TFG.apps.question.models import Question
from TFG.apps.subject.models import Subject
import datetime


class TestForm(forms.ModelForm):
    template_name = "subject_create.html"

    random_value = ('15', "Aleatorio")

    error_messages = dict(select_required=_("Debe seleccionar un modelo de examen"),
                          field_required=_("Es obligatorio rellenar el campo"),
                          positive_integer=_("El número debe de ser mayor que 0"),
                          number_type=_("Introduzca un número"),
                          invalid_datetime=_("La fecha introducida es inválida"),
                          )

    name = forms.CharField(required=True, label="Nombre del test")
    type = forms.ChoiceField(choices=Test.TYPES_CHOICES, initial=Test.STANDARD, label=_("Tipo de examen"),
                             required=True)
    type_question = forms.ChoiceField(choices=Question.TYPES_CHOICES, initial=Question.STANDARD,
                                      label=_("Tipo de preguntas"),
                                      required=True)
    autogenerate_questions = forms.BooleanField(required=True, initial=True,label=_("¿Preguntas aleatorias?"))
    num_question = forms.IntegerField(max_value=256, min_value=1, initial=1, required=True, label=_("Nº preguntas"))
    start_date = forms.DateField(required=False, label=_("Fecha de activación"),
                                 input_formats=['%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d'],
                                 widget=forms.DateInput(format='%d/%m/%Y'))
    end_date = forms.DateField(required=False, label=_("Fecha de finalización"),
                               input_formats=['%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d'],
                               widget=forms.DateInput(format='%d/%m/%Y'))
    duration = forms.IntegerField(help_text=_("Duración en minutos del test"), required=False,
                                  label=_("Duración (seg)"))
    activation_code = forms.CharField(required=False, label=_("Código de activación"))
    qr_code = forms.ImageField(required=False)
    visibility = forms.ChoiceField(choices=Test.VISIBILITY_CHOICES, required=True, label=_("Visibilidad"))
    active = forms.BooleanField(required=False, initial=True, label=_("¿Activar Test?"))
    created_on = forms.DateTimeField(required=False)

    class Meta:
        model = Test
        fields = "__all__"
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['subject'].empty_label = _("Seleccione una asignatura (obligatorio)")
        self.fields['topic'].empty_label = _("Todos")
        self.fields['subtopic'].empty_label = _("Todos")
        option_random = ('-1', _("Aleatorio"))
        # choices = self.fields['type_question'].insert(-1, (option_random))

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="field_required")
        return name

    def clean_type(self):
        type = self.cleaned_data['type']

        if not type:
            raise forms.ValidationError(
                self.error_messages['select_required'], code="select_required")
        return type

    def clean_num_question(self):
        num_question = self.cleaned_data['num_question']

        if num_question is not None:

            if int(num_question) <= 0:
                raise forms.ValidationError(
                    self.error_messages['positive_integer'], code="positive_number")
            return num_question

        raise forms.ValidationError(
            self.error_messages['field_required'], code="required")

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']

        if start_date is not None:
            if not isinstance(start_date, datetime.date):
                raise forms.ValidationError(
                    self.error_messages['invalid_datetime'], code="invalid_datetime")
            return start_date
        return None

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']

        if end_date is not None:
            if not isinstance(end_date, datetime.date):
                raise forms.ValidationError(
                    self.error_messages['invalid_datetime'], code="invalid_datetime")
            return end_date
        return None

    def clean_duration(self):
        duration = self.cleaned_data['duration']

        if duration is not None:
            # if not duration.is_digit():
            if duration <= 0:
                raise forms.ValidationError(
                    self.error_messages['number_type'], code="number_type")
                # return duration
        return None

    def clean_activation_code(self):
        activation_code = self.cleaned_data['activation_code']
        if activation_code is not None:
            return activation_code
        return None

    def clean_active(self):
        active = self.cleaned_data['active']
        if active is None:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="field_required")
        return active
