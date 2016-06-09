__author__ = 'oskyar'

from django import forms  # ModelForm, CharField, BooleanField, Textarea,NumberInput,
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from .models import Subject, Topic, Answer, Question


class CreateSubjectForm(forms.ModelForm):
    template_name = "create.html"

    error_messages = dict(field_required=_("Es obligatorio rellenar el campo"))

    name = forms.CharField(required=True, label="Nombre de la asignatura")
    description = forms.CharField(
        widget=forms.Textarea(attrs={'row': 1, 'class': 'materialize-textarea', 'length': '512'}), max_length=512,
        label=_('Escriba una breve descripción (máximo 512 caracteres)'))
    capacity = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 0, 'required': True}),
                               label=_("Nº Alumnos"))

    class Meta:
        model = Subject
        fields = ['name', 'description', 'capacity', 'test_opt', 'image']
        exclude = ['category']

    def clean_name(self):
        name = self.cleaned_data['name']
        print(name)
        if not name:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="required")
        return name

    def clean_image(self):
        image = self.cleaned_data['image']
        print(image)

    def clean_description(self):
        description = self.cleaned_data['description']
        if not description:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="required")
        return description


class CreateTopicForm(forms.ModelForm):
    template_name = "create.html"
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

    class Meta:
        model = Topic
        widgets = {
            'name': forms.TextInput(attrs={'class': 'validate'}),
            'cardinality': forms.TextInput(attrs={'class': 'validate'}),
            'description': forms.TextInput(attrs={'class': 'validate'}),
            'value': forms.TextInput(attrs={'class': 'validate'}),
        }
        fields = ['name', 'cardinality', 'description', 'value']


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
        print("Entra en el puto type")
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


class CreateAnswerForm(forms.ModelForm):
    reply = forms.CharField(required=True, label=_("Respuesta"), max_length=300)
    valid = forms.BooleanField(label=_("Haz check si es correcta la respuesta"), initial=False, required=False,
                               widget=forms.CheckboxInput(attrs={'class': 'valid-reply'}))
    adjustment = forms.IntegerField(label=_("Valor (%)"), max_value=100, min_value=0, initial=0, required=False)

    error_messages = dict(
        field_required=_("Es obligatorio rellenar el campo"),
        bad_value=_("El valor tiene que ser entre 0 y 100")
    )

    class Meta:
        model = Answer
        widgets = {
            'reply': forms.TextInput(attrs={'class': 'validate'})
        }
        fields = ['reply', 'valid']
        exclude = ['statistic', 'adjustment']
        # fields =['reply', 'valid', 'adjustment']

    def clean_reply(self):
        reply = self.cleaned_data.get('reply')
        if not reply:
            raise forms.ValidationError(
                self.error_messages['field_required'], code="required")

        return reply

    def clean_valid(self):
        return self.cleaned_data.get('valid') or False

    def clean_adjustment(self):
        value = self.cleaned_data.get('adjustment')
        if value > 100 or value < 0:
            raise forms.ValidationError(
                self.error_messages['bad_value'], code="bad_value")
        return value


class AnswerFormSet(BaseInlineFormSet):
    error_messages = dict(
        num_valids_incorrect=_("El número de respuestas correctas sólo puede ser 1"),
    )
    def clean(self):
        if self.data.get('type') is Question.STANDARD:
            num_valids = 0
            for num in range(0, 4):
                if self.data.get('answer-' + num + 'valid') is not None:
                    num_valids += 1
            if num_valids is not 1:
                raise forms.ValidationError(
                    self.error_messages['num_valids_incorrect'], code="bad_value")


InlineAnswerFormSet = inlineformset_factory(Question, Answer, form=CreateQuestionForm, formset=AnswerFormSet)
