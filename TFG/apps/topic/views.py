__author__ = 'oskyar'

from TFG.apps.subject.models import Subject
from TFG.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from vanilla import DetailView, ListView, DeleteView, UpdateView
from .forms import CreateTopicForm, CreateSubtopicForm
from .models import Topic, Subtopic
from guardian.shortcuts import assign_perm


class CreateTopicView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = CreateTopicForm

    def get_context_data(self, **kwargs):
        context = super(CreateTopicView, self).get_context_data(**kwargs)
        subject = Subject.objects.get(pk=self.kwargs['pk'])
        context['subject'] = subject
        context['topics'] = Topic.objects.filter(subject=subject)
        context['breadcrumbs'] = self.get_breadcrumbs(subject)
        return context

    def get_template_names(self):
        if 'pk_topic' in self.kwargs:
            return "subtopic/subtopic_create.html"
        else:
            return "topic/topic_create.html"

    def get_initial(self):
        initial = super(CreateTopicView, self).get_initial()
        subject = Subject.objects.get(pk=self.kwargs.get('pk'))
        initial['cardinality'] = self.get_min_cardinality_empty(subject.topics.all())
        initial['value'] = 100
        return initial

    def form_valid(self, form):

        topic = form.save(commit=False)

        # Como se comparte form y vista para topic y subtopic, hay que tenerlos en cuenta.
        if 'pk_topic' in self.kwargs:
            topic.topic = self.kwargs.get('pk_topic')
        else:
            topic.subject = Subject.objects.get(pk=self.kwargs['pk'])
        topic.save()
        assign_perm('topic.add_topic', self.request.user, topic)
        assign_perm('topic.change_topic', self.request.user, topic)
        assign_perm('topic.delete_topic', self.request.user, topic)
        # Comprobamos a qué botón de submit le hemos dado
        if 'create_subtopic' in self.request.POST:
            kwargs = self.kwargs
            return redirect("create_subtopic", pk=self.kwargs['pk'], pk_topic=topic.pk)
        else:
            return redirect("create_topic", pk=self.kwargs['pk'])

    def form_invalid(self, form):
        return super(CreateTopicView, self).form_invalid(form)

    def get_breadcrumbs(self, subject):
        breadcrumbs = list()
        breadcrumbs.append(
            {"url": "/", "title": "Inicio", "tooltip": "Inicio"})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_subject', kwargs={'pk': self.kwargs.get('pk')}), "title": subject.name,
             "tooltip": _("Asignatura")})
        breadcrumbs.append(
            {"url": "#", "title": _("Crear TEMA"),
             "tooltip": _("Crear Tema")})
        return breadcrumbs

    def get_min_cardinality_empty(self, topics):
        cardinalities = set([topic.cardinality for topic in topics])
        if cardinalities:
            max_cardinality = max(cardinalities)
            range_cardinalities = set(range(1, max_cardinality + 2))
            min_cardinality_available = min(range_cardinalities - cardinalities)
            return min_cardinality_available
        else:
            return 1


class UpdateTopicView(UpdateView):
    form_class = CreateTopicForm
    fields = "__all__"
    template_name = "topic/topic_create.html"
    context_object_name = 'topic'

    def get_object(self):
        return Topic.objects.get(pk=self.kwargs.get('pk_topic'))

    def get_context_data(self, **kwargs):
        context = super(UpdateTopicView, self).get_context_data(**kwargs)
        subject = Subject.objects.get(pk=self.kwargs['pk'])
        context['subject'] = subject
        context['topics'] = Topic.objects.filter(subject=subject)
        context['breadcrumbs'] = self.get_breadcrumbs(subject)
        context['edit'] = True
        return context

    def form_valid(self, form):

        topic = form.save(commit=False)

        # Como se comparte form y vista para topic y subtopic, hay que tenerlos en cuenta.
        if 'pk_topic' in self.kwargs:
            topic.topic = self.kwargs.get('pk_topic')
        else:
            topic.subject = Subject.objects.get(pk=self.kwargs['pk'])
        topic.save()

        # Comprobamos a qué botón de submit le hemos dado
        if 'create_subtopic' in self.request.POST:
            kwargs = self.kwargs
            return redirect("create_subtopic", pk=self.kwargs['pk'], pk_topic=topic.pk)
        else:
            return redirect("create_topic", pk=self.kwargs['pk'])

    def form_invalid(self, form):
        return super(CreateTopicView, self).form_invalid(form)

    def get_breadcrumbs(self, subject):
        breadcrumbs = list()
        breadcrumbs.append(
            {"url": "/", "title": "Inicio", "tooltip": "Inicio"})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_subject', kwargs={'pk': self.kwargs.get('pk')}), "title": subject.name,
             "tooltip": _("Asignatura")})
        breadcrumbs.append(
            {"url": "#", "title": _("Crear TEMA"),
             "tooltip": _("Crear Tema")})
        return breadcrumbs


class DetailTopicView(DetailView):
    template_name = 'topic/topic_detail.html'
    lookup_field = 'pk_topic'

    def get_object(self):
        return Topic.objects.get(pk=self.kwargs.get('pk_topic'))

    def get_context_data(self, **kwargs):
        context = super(DetailTopicView, self).get_context_data(**kwargs)
        topic = Topic.objects.get(pk=self.kwargs.get('pk_topic'))
        context['topic'] = topic
        context['breadcrumbs'] = self.get_breadcrumbs(topic)
        return context

    def get_breadcrumbs(self, topic):
        breadcrumbs = list()
        breadcrumbs.append(
            {"url": "/", "title": "Inicio", "tooltip": "Inicio"})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_subject', kwargs={'pk': topic.subject.id}), "title": topic.subject.name,
             "tooltip": _("Asignatura")})
        breadcrumbs.append(
            {"url": "#", "title": topic.name, "tooltip": _("Tema")})
        return breadcrumbs


class ListTopicView(ListView):
    model = Topic

    def get_object(self):
        return Subject.objects.get(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(ListTopicView, self).get_context_data(**kwargs)
        subject = Subject.objects.get(pk=self.kwargs.get('pk'))
        context['breadcrumbs'] = self.get_breadcrumbs(subject)
        return context

    def get_breadcrumbs(self, subject):
        breadcrumbs = list()
        breadcrumbs.append(
            {"url": "/", "title": "Inicio", "tooltip": "Inicio"})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_subject', kwargs={'pk': subject.id}), "title": subject.name,
             "tooltip": _("Asignatura")})
        breadcrumbs.append(
            {"url": "#", "title": _("Lista de temas"), "tooltip": _("Lista temas")})
        return breadcrumbs


class DeleteTopicView(LoginRequiredMixin, DeleteView):
    model = Topic
    success_url = reverse_lazy('/')

    def get(self, request, *args, **kwargs):
        topic = Topic.objects.get(pk=self.kwargs.get('pk_topic'))
        owner = topic.subject.teacher.user
        if not self.request.is_ajax() and self.request.user == owner:
            get_object_or_404(Topic, pk=topic.id).delete()
            result = {'success': True}
            return redirect(reverse_lazy('detail_subject', kwargs=self.kwargs))

    def post(self, request, *args, **kwargs):
        topic = Topic.objects.get(pk=self.kwargs.get('pk_topic'))
        owner = topic.subject.teacher.user
        if self.request.is_ajax() and self.request.user == owner:
            get_object_or_404(Topic, pk=topic.id).delete()
            result = {'success': True}
            return JsonResponse(result)


class CreateSubtopicView(LoginRequiredMixin, CreateView):
    template_name = 'subtopic/subtopic_create.html'
    model = Subtopic
    form_class = CreateSubtopicForm

    def get_context_data(self, **kwargs):
        context = super(CreateSubtopicView, self).get_context_data(**kwargs)
        topic = Topic.objects.get(pk=self.kwargs['pk_topic'])
        context['subject'] = topic.subject
        context['topic'] = topic
        context['subtopics'] = Subtopic.objects.filter(topic=topic)
        context['breadcrumbs'] = self.get_breadcrumbs(topic)
        return context

    def get_initial(self):
        initial = super(CreateSubtopicView, self).get_initial()
        topic = Topic.objects.get(pk=self.kwargs.get('pk_topic'))
        initial['cardinality'] = self.get_min_cardinality_empty(topic.subtopics.all())
        initial['value'] = 100
        return initial

    def form_valid(self, form):

        subtopic = form.save(commit=False)
        # Como se comparte form y vista para topic y subtopic, hay que tenerlos en cuenta.
        subtopic.topic = Topic.objects.get(pk=self.kwargs.get('pk_topic'))
        subtopic.save()
        assign_perm('topic.add_subtopic', self.request.user, subtopic)
        assign_perm('topic.change_subtopic', self.request.user, subtopic)
        assign_perm('topic.delete_subtopic', self.request.user, subtopic)
        # Comprobamos a qué botón de submit le hemos dado
        if 'create_subtopic' in self.request.POST:
            return redirect("create_subtopic", pk=subtopic.topic.subject.pk, pk_topic=subtopic.topic.pk)
        else:

            return redirect("create_question", pk=subtopic.topic.subject.pk, pk_topic=subtopic.topic.pk,
                            pk_subtopic=subtopic.pk)

    def form_invalid(self, form):
        return super(CreateSubtopicView, self).form_invalid(form)

    def get_min_cardinality_empty(self, subtopics):
        cardinalities = set([subtopic.cardinality for subtopic in subtopics])
        if cardinalities:
            max_cardinality = max(cardinalities)
            range_cardinalities = set(range(1, max_cardinality + 2))
            min_cardinality_available = min(range_cardinalities - cardinalities)
            return min_cardinality_available
        else:
            return 1

    def get_breadcrumbs(self, topic):
        breadcrumbs = list()
        breadcrumbs.append(
            {"url": "/", "title": "Inicio", "tooltip": "Inicio"})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_subject', kwargs={'pk': self.kwargs.get('pk')}), "title": topic.subject.name,
             "tooltip": _("Asignatura")})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_topic',
                                 kwargs={'pk': topic.subject.id, 'pk_topic': topic.id}),
             "title": topic.name,
             "tooltip": _("Tema")})
        breadcrumbs.append(
            {"url": "#",
             "title": _("Crear subtema"),
             "tooltip": _("Crear Subtema")})

        return breadcrumbs


class UpdateSubtopicView(UpdateView):
    form_class = CreateSubtopicForm
    fields = "__all__"
    template_name = "subtopic/subtopic_create.html"
    lookup_field = 'pk_subtopic'

    def get_object(self):
        return Subtopic.objects.get(pk=self.kwargs.get('pk_subtopic'))

    def get_context_data(self, **kwargs):
        context = super(UpdateSubtopicView, self).get_context_data(**kwargs)
        subtopic = Subtopic.objects.get(pk=self.kwargs['pk_subtopic'])
        context['subject'] = subtopic.topic.subject
        context['topic'] = subtopic.topic
        context['subtopic'] = subtopic
        context['subtopics'] = subtopic.topic.subtopics.all()
        context['breadcrumbs'] = self.get_breadcrumbs(subtopic.topic)
        context['edit'] = True
        return context

    def form_valid(self, form):

        subtopic = form.save(commit=False)
        # Como se comparte form y vista para topic y subtopic, hay que tenerlos en cuenta.
        subtopic.topic = Topic.objects.get(pk=self.kwargs.get('pk_topic'))
        subtopic.save()

        # Comprobamos a qué botón de submit le hemos dado
        if 'create_subtopic' in self.request.POST:
            return redirect("create_subtopic", pk=subtopic.topic.subject.pk, pk_topic=subtopic.topic.pk)
        else:

            return redirect("create_question", pk=subtopic.topic.subject.pk, pk_topic=subtopic.topic.pk,
                            pk_subtopic=subtopic.pk)

    def form_invalid(self, form):
        return super(UpdateSubtopicView, self).form_invalid(form)

    def get_breadcrumbs(self, topic):
        breadcrumbs = list()
        breadcrumbs.append(
            {"url": "/", "title": "Inicio", "tooltip": "Inicio"})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_subject', kwargs={'pk': self.kwargs.get('pk')}), "title": topic.subject.name,
             "tooltip": _("Asignatura")})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_topic',
                                 kwargs={'pk': topic.subject.id, 'pk_topic': topic.id}),
             "title": topic.name,
             "tooltip": _("Tema")})
        breadcrumbs.append(
            {"url": "#",
             "title": _("Crear subtema"),
             "tooltip": _("Crear Subtema")})

        return breadcrumbs


class ListSubtopicView(ListView):
    template_name = "subtopic/subtopic_list.html"

    pass


class DetailSubtopicView(DetailView):
    template_name = "subtopic/subtopic_detail.html"
    lookup_field = "pk_subtopic"
    context_object_name = 'subtopic'

    def get_object(self):
        return Subtopic.objects.get(pk=self.kwargs.get('pk_subtopic'))

    def get_context_data(self, **kwargs):
        context = super(DetailSubtopicView, self).get_context_data(**kwargs)
        subtopic = Subtopic.objects.get(pk=self.kwargs.get('pk_subtopic'))
        context['breadcrumbs'] = self.get_breadcrumbs(subtopic)
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
            {"url": "#",
             "title": subtopic.name,
             "tooltip": _("Subtema")})

        return breadcrumbs


class DeleteSubtopicView(LoginRequiredMixin, DeleteView):
    model = Subtopic
    success_url = "/"

    def get(self, request, *args, **kwargs):
        subtopic = Subtopic.objects.get(pk=self.kwargs.get('pk_subtopic'))
        owner = subtopic.topic.subject.teacher.user
        if not self.request.is_ajax() and self.request.user == owner:
            get_object_or_404(Subtopic, pk=subtopic.pk).delete()
            result = {'success': True}
            return redirect(reverse_lazy('detail_topic',
                                         kwargs={'pk': self.kwargs.get('pk'), 'pk_topic': self.kwargs.get('pk_topic')}))

    def post(self, request, *args, **kwargs):
        subtopic = Subtopic.objects.get(pk=self.kwargs.get('pk_subtopic'))
        owner = subtopic.topic.subject.teacher.user
        if self.request.is_ajax() and self.request.user == owner:
            get_object_or_404(Subtopic, pk=subtopic.pk).delete()
            result = {'success': True}
            return JsonResponse(result)
        else:
            return super(DeleteSubtopicView, self).post(request, *args, **kwargs)
