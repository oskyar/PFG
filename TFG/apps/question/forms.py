__author__ = 'oskyar'

from django import forms  # ModelForm, CharField, BooleanField, Textarea,NumberInput,
from django.utils.translation import ugettext_lazy as _
from .models import Question

class CreateQuestionForm(forms.ModelForm):
    statement = forms.CharField(required=True, label=_("Enunciado de la pregunta"), max_length=150)
    type = forms.ChoiceField(choices=Question.TYPES_CHOICES, initial=0, label=_("Tipo de pregunta"))



    error_messages = dict(
        field_required=_("Es obligatorio rellenar el campo"),
    )

    class Meta:
        model = Question
        widgets = {
            'statement': forms.TextInput(attrs={'class': 'validate'}),
        }
        fields = ['statement', 'type']

    def clean_type(self):
        type = self.cleaned_data['type']
        if not type:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="required")
        return type

    def clean_statement(self):
        statement = self.cleaned_data['statement']
        if not statement:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="required")
        return statement

