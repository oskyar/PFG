__author__ = 'oskyar'

from TFG.apps.answer.forms import InlineAnswerFormSet, AnswerInline
from TFG.apps.topic.models import Topic, Subtopic
from TFG.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView
from extra_views import CreateWithInlinesView
from .forms import CreateQuestionForm
from .models import Question
from guardian.shortcuts import assign_perm


class CreateQuestionView(LoginRequiredMixin, CreateWithInlinesView):
    model = Question
    inlines = [AnswerInline]
    form_class = CreateQuestionForm
    success_url = '/'
    template_name = "question/question_create.html"

    def forms_valid(self, form, inlines):
        # response = super(CreateQuestionView, self).forms_valid(form, inlines)

        question_form = form.save(commit=False)
        question_form.subtopic = Subtopic.objects.get(pk=self.kwargs['pk_subtopic'])
        inline_answer_form = InlineAnswerFormSet(self.request.POST, instance=question_form)
        if inline_answer_form.is_valid():
            question_form.save()
            inline_answer_form.save()

        assign_perm('question.add_question', self.request.user, question_form)
        assign_perm('question.change_question', self.request.user, question_form)
        assign_perm('question.delete_question', self.request.user, question_form)
        # inlineAnswer = InlineAnswerFormSet(parent_model=Question, request=self.request, instance=question)
        # questionFormSet = inlineAnswer.get_formset()


        response = super(CreateQuestionView, self).forms_valid(form, inlines)
        return response

    def forms_invalid(self, form, inlines):
        context = super(CreateQuestionView, self).forms_invalid(form, inlines)
        # inline_answer_form = InlineAnswerFormSet(self.request.POST, instance=form)

        return context
        # super(CreateQuestionView, self).forms_invalid(form, inlines)

    def get_success_url(self):
        return reverse_lazy("create_question",
                            kwargs={'pk': self.kwargs['pk'], 'pk_topic': self.kwargs['pk_topic'],
                                    'pk_subtopic': self.kwargs['pk_subtopic']})

    def get_context_data(self, **kwargs):
        context = super(CreateQuestionView, self).get_context_data(**kwargs)
        current_subtopic = Subtopic.objects.get(pk=self.kwargs['pk_subtopic'])
        context['current_subtopic'] = current_subtopic
        context['subtopics'] = Subtopic.objects.filter(topic=Topic.objects.get(pk=self.kwargs['pk_topic']))
        questions = list(Subtopic.objects.get(pk=self.kwargs['pk_subtopic']).questions.all())
        for question in questions:
            question.answers = question.answer.all()
        context['questions'] = questions
        context['breadcrumbs'] = self.get_breadcrumbs(current_subtopic)
        return context

    def get_breadcrumbs(self, subtopic):
        breadcrumbs = list()
        breadcrumbs.append(
            {"url": "/", "title": "Inicio", "tooltip": "Inicio"})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_subject', kwargs={'pk': subtopic.topic.subject.id}),
             "title": subtopic.topic.subject.name,
             "tooltip": _("Asignatura")})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_topic',
                                 kwargs={'pk': subtopic.topic.subject.id, 'pk_topic': subtopic.topic.id}),
             "title": subtopic.topic.name,
             "tooltip": _("Tema")})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_subtopic',
                                 kwargs={'pk': subtopic.topic.subject.id, 'pk_topic': subtopic.topic.id,
                                         'pk_subtopic': subtopic.id}), "title": subtopic.name, "tooltip": _("Subtema")})

        breadcrumbs.append(
            {"url": "#", "title": _("Crear preguntas"), "tooltip": _("Preguntas")})

        return breadcrumbs


class DeleteQuestionView(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('/')

    def post(self, request, *args, **kwargs):
        owner = Question.objects.get(pk=self.kwargs.get('pk_question')).subtopic.topic.subject.teacher.user
        if self.request.is_ajax() and self.request.user == owner:
            get_object_or_404(Question, pk=self.kwargs['pk_question']).delete()
            result = {'success': True}
            return JsonResponse(result)
