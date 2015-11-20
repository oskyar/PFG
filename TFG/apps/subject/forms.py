__author__ = 'oskyar'

from django import forms  # ModelForm, CharField, BooleanField, Textarea,NumberInput,
from django.utils.translation import ugettext_lazy as _
from .models import Subject
from django.contrib.auth.models import User


class CreateSubjectForm(forms.ModelForm):
    template_name = "create.html"
    name = forms.CharField(required=True, label="Nombre de la asignatura")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'row': 1, 'class': 'materialize-textarea', 'length': '512'}), max_length=512,
        label=_('Escriba una breve descripción (máximo 512 caracteres)'))
    capacity = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 0, 'required': True}),
                               label=_("Nº Alumnos"))

    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['category', 'teacher']
