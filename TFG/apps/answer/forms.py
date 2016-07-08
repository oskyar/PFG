__author__ = 'oskyar'

from TFG.apps.question.forms import CreateQuestionForm
from TFG.apps.question.models import Question
from django import forms  # ModelForm, CharField, BooleanField, Textarea,NumberInput,
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
# from extra_views.formsets import InlineFormSetView
from extra_views import InlineFormSet
from .models import Answer


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
        num_questions_incorrect=_("El número de respuestas debe de ser 4"),
    )

    def clean(self):

        if int(self.data.get('type')) is Question.STANDARD or int(self.data.get('type')) is Question.MULTIPLE:
            num_replies = 0
            for num in range(0, 4):
                if self.data.get('answer-' + str(num) + '-reply') is not None:
                    num_replies += 1
            if num_replies is not 4:
                raise forms.ValidationError(
                    self.error_messages['num_questions_incorrect'], code="bad_num_questions")

        if int(self.data.get('type')) is Question.STANDARD:
            num_valids = 0
            num_replies = 0
            for num in range(0, 4):
                if self.data.get('answer-' + str(num) + '-valid') is not None:
                    num_valids += 1
            if num_valids is not 1:
                raise forms.ValidationError(
                    self.error_messages['num_valids_incorrect'], code="bad_value")


class AnswerInline(InlineFormSet):
    model = Answer
    extra = 4
    max_num = 4
    can_delete = False
    form_class = CreateAnswerForm


#InlineAnswerFormSet = inlineformset_factory(Question, Answer, form=CreateQuestionForm, formset=AnswerFormSet)
InlineAnswerFormSet = inlineformset_factory(Question, Answer, form=CreateAnswerForm, formset=AnswerFormSet)
