__author__ = 'oskyar'

from django import forms  # ModelForm, CharField, BooleanField, Textarea,NumberInput,
from django.utils.translation import ugettext_lazy as _
from .models import Topic, Subtopic


class CreateTopicForm(forms.ModelForm):
    template_name = "subject_create.html"
    error_messages = dict(
        field_required=_("Es obligatorio rellenar el campo"),
        cardinality_not_consecutive=_("La cardinalidad debe de ser consecutiva entre temas (1, 2 ,3...)"),
        duplicate_number=_("Número duplicado")
    )
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'validate'}),
                           label=_("Nombre del tema"))
    cardinality = forms.IntegerField(label=_("Nº"))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'row': 1, 'class': 'materialize-textarea', 'length': '512'}), max_length=512,
        label=_('Escriba una breve descripción (máximo 512 caracteres)'))

    value = forms.IntegerField(required=True, label=_("Ponderación"),
                               help_text=_(
                                   "Este valor será definido automáticamente en caso de no asignarle uno, será la media de dividir 100 entre todos los temas creados."))
    gamificar = forms.BooleanField(required=False, label=_("¿Gamificar?"), help_text=_(
        "Al seleccionar que sí, el Tema se mostrará  en el sistema gamificado."), initial=True)

    class Meta:
        model = Topic
        widgets = {
            'name': forms.TextInput(attrs={'class': 'validate'}),
            'cardinality': forms.TextInput(attrs={'class': 'validate'}),
            'description': forms.TextInput(attrs={'class': 'validate'}),
            'value': forms.TextInput(attrs={'class': 'validate'}),
        }
        fields = ['name', 'cardinality', 'description', 'value', 'gamificar']

    def clean_name(self):
        name = self.cleaned_data['name']
        if name is None:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="field_required")
        return name

    def clean_cardinality(self):
        cardinality = self.cleaned_data['cardinality']
        if cardinality is None:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="field_required")
        return cardinality

    def clean_description(self):
        description = self.cleaned_data['description']
        if description is None:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="field_required")
        return description

    def clean_value(self):
        value = self.cleaned_data['value']
        if value is None:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="field_required")
        return value


class CreateSubtopicForm(forms.ModelForm):
    template_name = "subject_create.html"
    error_messages = dict(
        field_required=_("Es obligatorio rellenar el campo"),
    )
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'validate'}),
                           label=_("Nombre del tema"))
    cardinality = forms.IntegerField(label=_("Nº"))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'row': 1, 'class': 'materialize-textarea', 'length': '512'}), max_length=512,
        label=_('Escriba una breve descripción (máximo 512 caracteres)'))

    value = forms.IntegerField(required=True, label=_("Ponderación"),
                               help_text=_(
                                   "Este valor será definido automáticamente en caso de no asignarle uno, será la media de dividir 100 entre todos los temas creados."))
    gamificar = forms.BooleanField(required=False, label=_("¿Gamificar?"), help_text=_(
        "Al seleccionar que sí, el subtema se mostrará  en el sistema gamificado."), initial=True)

    class Meta:
        model = Subtopic
        widgets = {
            'name': forms.TextInput(attrs={'class': 'validate'}),
            'cardinality': forms.TextInput(attrs={'class': 'validate'}),
            'description': forms.TextInput(attrs={'class': 'validate'}),
            'value': forms.TextInput(attrs={'class': 'validate'}),
        }
        fields = ['name', 'cardinality', 'description', 'value', 'gamificar']

    def clean_name(self):
        name = self.cleaned_data['name']
        if name is None:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="field_required")
        return name

    def clean_cardinality(self):
        cardinality = self.cleaned_data['cardinality']
        if cardinality is None:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="field_required")
        return cardinality

    def clean_description(self):
        description = self.cleaned_data['description']
        if description is None:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="field_required")
        return description

    def clean_value(self):
        value = self.cleaned_data['value']
        if value is None:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="field_required")
        return value
