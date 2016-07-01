__author__ = 'oskyar'

from django import forms
from django.utils.translation import ugettext_lazy as _
from s3direct.fields import S3DirectWidget
from .models import Subject


class CreateSubjectForm(forms.ModelForm):
    template_name = "subject_create.html"

    error_messages = dict(field_required=_("Es obligatorio rellenar el campo"))

    name = forms.CharField(required=True, label="Nombre de la asignatura")
    description = forms.CharField(max_length=512,
                                  label=_('Escriba una breve descripción (máximo 512 caracteres)'))
    capacity = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 0, 'required': True}),
                               label=_("Nº máx. alumnos"))
    category = forms.CharField(required=True, label="Categoría")

    image = forms.URLField(widget=S3DirectWidget(dest='subject', html=(
        '<div class="s3direct" data-policy-url="{policy_url}">'
        '  <a class="file-link" target="_blank" src="{file_url}" >{file_name}</a>'
        '  <input class="file-url" type="hidden" value="{file_url}" id="{element_id}" name="{name}" />'
        '  <input class="file-dest" type="hidden" value="{dest}">'
        '  <input class="file-input input-field btn" type="file" />'
        '  <a class="file-remove btn orange" href="#remove">Remove</a>'
        '  <div class="progress progress-striped active">'
        '    <div class="bar"></div>'
        '  </div>'
        '</div>'
    )), required=False, label=_("Imagen asignatura"))

    class Meta:
        model = Subject
        fields = ['name', 'description', 'capacity', 'test_opt', 'image', 'category']
        exclude = ['created_on']

    def clean_name(self):
        name = self.cleaned_data['name']
        print(name)
        if not name:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="required")
        return name

    def clean_image(self):
        image = self.cleaned_data['image']
        return image

    def clean_description(self):
        description = self.cleaned_data['description']
        if not description:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="required")
        return description

    def clean_capacity(self):
        capacity = self.cleaned_data['capacity']
        if not capacity and capacity == 0:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="required")
        return capacity

    def clean_category(self):
        category = self.cleaned_data['category']
        if not category:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="required")
        return category
