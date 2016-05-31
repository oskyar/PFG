__author__ = 'oskyar'

from TFG.mixins import LoginRequiredMixin
from ajaxuploader.views import AjaxFileUploader
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, FormView, ListView, DeleteView
from .forms import CreateSubjectForm, CreateTopicForm, CreateQuestionForm, AnswerFormSet, CreateAnswerForm
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


class CreateQuestionView(LoginRequiredMixin, FormView):
    template_name = 'question/create.html'
    form_class = CreateQuestionForm

    def get_context_data(self, **kwargs):
        context = super(CreateQuestionView, self).get_context_data(**kwargs)
        context['current_topic'] = Topic.objects.get(pk=self.kwargs['pk_topic'])
        context['topics'] = Topic.objects.filter(subject=Subject.objects.get(pk=self.kwargs['pk_subject']))
        context['replies_form'] = AnswerFormSet(self.request.POST or None, prefix='replies_form')

        questions = list(Topic.objects.get(pk=self.kwargs['pk_topic']).question.all())
        for question in questions:
            question.answers = question.answer.all()
        context['questions'] = questions
        return context

    def post(self, request, *args, **kwargs):
        replies_form = AnswerFormSet(self.request.POST)
        for f in replies_form:
            cd = f.cleaned_data

    def form_valid(self, form):
        print("Form valido")
        context = self.get_context_data()
        replies_context = context['replies_form']


        replies_form = AnswerFormSet(self.request.POST)
        question = form.save(commit=False)
        question.topic = Topic.objects.get(pk=self.kwargs['pk_topic'])

        # TODO: lanzar CLEAN y si valid = None ponerlo a False y si es 'on' ponerlo a True
        replies_form.clean()
        if replies_form.is_valid():
            a1 = CreateAnswerForm(reply=form.data.get('id_form-0-reply'), valid=valid0,
                                  adjustment=form.data.get('id_form-0-adjustement'))
            a1.is_valid()
            Answer.objects.create(question=question, reply=form.data.get('id_form-1-reply'), valid=valid1,
                                  adjustment=form.data.get('id_form-1-adjustement'))
            Answer.objects.create(question=question, reply=form.data.get('id_form-2-reply'), valid=valid2,
                                  adjustment=form.data.get('id_form-2-adjustement'))
            Answer.objects.create(question=question, reply=form.data.get('id_form-3-reply'), valid=valid3,
                                  adjustment=form.data.get('id_form-3-adjustement'))
            question.save()
            return redirect("create_question", pk_subject=self.kwargs['pk_subject'], pk_topic=self.kwargs['pk_topic'])
        else:
            print("Entra en el else")
            return redirect("create_question", pk_subject=self.kwargs['pk_subject'], pk_topic=self.kwargs['pk_topic'])

            # return redirect("create_topic", pk=subject.id)
            # return super(CreateTopicView, self).form_valid(form)

    def form_invalid(self, form):

        print("form Invalido")
        return super(CreateQuestionView, self).form_invalid(form)

    """
    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        replies_form = AnswerFormSet()
        context = self.get_context_data(form=form, replies_form=replies_form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        ""
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        ""
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        replies_form = AnswerFormSet(self.request.POST)
        if (form.is_valid() and replies_form.is_valid()):
            return self.form_valid(form, replies_form)
        else:
            return self.form_invalid(form, replies_form)
    """


# TODO: Seguir por aquí, creando el método de borrar.
"""def delete_question(request, id):
    note = get_object_or_404(Question, pk=id).delete()
    return HttpResponseRedirect(reverse('subject.views.notes'))
"""


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
