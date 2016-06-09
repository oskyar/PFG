__author__ = 'oskyar'

from TFG.mixins import LoginRequiredMixin
from ajaxuploader.views import AjaxFileUploader
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, ListView, DeleteView
from extra_views import CreateWithInlinesView, InlineFormSet
from .forms import CreateSubjectForm, CreateTopicForm, CreateQuestionForm, InlineAnswerFormSet, CreateAnswerForm
from .models import Subject, UserProfile, Topic, Answer, Question


class CreateSubjectView(LoginRequiredMixin, CreateView):
    template_name = 'subject/create.html'
    form_class = CreateSubjectForm
    success_url = "/"

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(CreateSubjectView, self).get_initial()
        # TODO: Quitar inicialización del nombre
        initial['name'] = "probando con imagen"
        initial['capacity'] = "10"
        initial['description'] = "Descripción de la asignatura en la que se intenta subir una imagen."
        return initial

    def form_valid(self, form):
        subject = form.save(commit=False)
        subject.teacher = UserProfile.objects.get_user_by_username(self.request.user)
        subject.category = "Prueba"
        subject.save()
        # return redirect("/subject/"+str(subject.id)+"/topic/create")

        # return redirect("create_topic", pk=subject.id)
        return super(CreateSubjectView, self).form_valid(form)

    def form_invalid(self, form):
        return super(CreateSubjectView, self).form_invalid(form)

    # @method_decorator(csrf_except)

    def dispatch(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        self.token = csrf_token
        return super(CreateSubjectView, self).dispatch(request, *args,
                                                       **kwargs)  # Método que sirve para la inserción de imágenes por medio de Ajax

    def get_success_url(self):
        return reverse_lazy("create_topic", kwargs={'pk': self.object.id})


class ListSubjectView(LoginRequiredMixin, ListView):
    template_name = 'subject/list.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        subjects = list(Subject.objects.filter(teacher=self.request.user.userProfile))
        for subject in subjects:
            subject.num_topics = len(subject.topics.all())
        return subjects


class CreateTopicView(LoginRequiredMixin, CreateView):
    template_name = 'topic/create.html'
    form_class = CreateTopicForm

    def get_context_data(self, **kwargs):
        context = super(CreateTopicView, self).get_context_data(**kwargs)
        subject = Subject.objects.get(pk=self.kwargs['pk'])
        context['subject'] = subject
        context['topics'] = Topic.objects.filter(subject=subject)
        return context

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.subject = Subject.objects.get(pk=self.kwargs['pk'])
        topic.save()
        return redirect("create_topic", pk=self.kwargs['pk'])

        # return redirect("create_topic", pk=subject.id)
        # return super(CreateTopicView, self).form_valid(form)

    def form_invalid(self, form):
        return super(CreateTopicView, self).form_invalid(form)


class AnswerInline(InlineFormSet):
    model = Answer
    extra = 4
    max_num = 4
    can_delete = False
    form_class = CreateAnswerForm
    # form_class = CreateAnswerForm


class CreateQuestionView(LoginRequiredMixin, CreateWithInlinesView):
    model = Question
    inlines = [AnswerInline]
    form_class = CreateQuestionForm
    success_url = '/'
    template_name = "question/create.html"

    def forms_valid(self, form, inlines):
        # response = super(CreateQuestionView, self).forms_valid(form, inlines)

        question_form = form.save(commit=False)
        question_form.topic = Topic.objects.get(pk=self.kwargs['pk_topic'])
        inline_answer_form = InlineAnswerFormSet(self.request.POST, instance=question_form)
        if inline_answer_form.is_valid():
            question_form.save()
            inline_answer_form.save()
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
                            kwargs={'pk_subject': self.kwargs['pk_subject'], 'pk_topic': self.kwargs['pk_topic']})

    def get_context_data(self, **kwargs):
        context = super(CreateQuestionView, self).get_context_data(**kwargs)
        context['current_topic'] = Topic.objects.get(pk=self.kwargs['pk_topic'])
        context['topics'] = Topic.objects.filter(subject=Subject.objects.get(pk=self.kwargs['pk_subject']))
        """replies_form = list()
        for i in range(4):
            replies_form.append(CreateAnswerForm(self.request.POST or None, prefix='reply-%s' % (i)))
        context['replies_form'] = replies_form
        """

        questions = list(Topic.objects.get(pk=self.kwargs['pk_topic']).question.all())
        for question in questions:
            question.answers = question.answer.all()
        context['questions'] = questions
        return context

class DeleteQuestionView(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('/')

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            get_object_or_404(Question, pk=self.kwargs['pk_question']).delete()
            result = {'success': True}
            return JsonResponse(result)


def delete_question(request):
    print("Entra aqui")
    get_object_or_404(Question, pk=int(self.request.REQUEST['id'])).delete()
    result = {'success': True}
    return HttpResponse(json.dumps(result), content_type='application/json')


def start(request):
    return render_to_response('import.html',
                              {'csrf_token': csrf_token}, context_instance=RequestContext(request))


import_uploader = AjaxFileUploader()
