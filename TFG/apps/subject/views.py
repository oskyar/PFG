__author__ = 'oskyar'

from TFG.apps.user.models import UserProfile
from TFG.mixins import LoginRequiredMixin
from ajaxuploader.views import AjaxFileUploader
from django.core.urlresolvers import reverse_lazy
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from vanilla import DetailView, RedirectView, UpdateView, DeleteView, ListView, CreateView
from .forms import CreateSubjectForm
from .models import Subject
from django.utils import timezone
from braces import views
from guardian.shortcuts import assign_perm


class CreateSubjectView(LoginRequiredMixin, CreateView):
    template_name = 'subject/subject_create.html'
    form_class = CreateSubjectForm
    success_url = "/"

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(CreateSubjectView, self).get_initial()
        # TODO: Quitar inicialización del nombre
        # initial['name'] = "probando con imagen"
        # initial['capacity'] = "10"
        # initial['description'] = "Descripción de la asignatura en la que se intenta subir una imagen."
        return initial

    def form_valid(self, form):
        subject = form.save(commit=False)
        subject.teacher = self.request.user.userProfile
        subject.created_on = timezone.now()
        subject.save()
        assign_perm('subject.add_subject', self.request.user, subject)
        assign_perm('subject.change_subject', self.request.user, subject)
        assign_perm('subject.delete_subject', self.request.user, subject)
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

    def get_breadcrumbs(self, subject):
        breadcrumbs = list()
        breadcrumbs.append(
            {"url": "/", "title": "Inicio", "tooltip": "Inicio"})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_subject', kwargs={'pk': self.kwargs.get('pk')}), "title": subject.name,
             "tooltip": _("Asignatura")})
        return breadcrumbs


class UpdateSubjectView(LoginRequiredMixin, views.PermissionRequiredMixin, UpdateView):
    form_class = CreateSubjectForm
    fields = "__all__"
    template_name = "subject/subject_create.html"
    context_object_name = 'subject'
    lookup_field = 'pk'
    permission_required = "subject.change_subject"

    def get_object(self):
        return Subject.objects.get(pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(UpdateSubjectView, self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def form_valid(self, form):
        subject = form.save(commit=False)
        subject.teacher = self.request.user.userProfile

        subject.save()
        # return redirect("/subject/"+str(subject.id)+"/topic/create")

        # return redirect("create_topic", pk=subject.id)
        return super(UpdateSubjectView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UpdateSubjectView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("create_topic", kwargs={'pk': self.object.id})


class DetailSubjectView(DetailView):
    model = Subject
    template_name = "subject/subject_detail.html"
    lookup_field = 'pk'

    def get_context_data(self, **kwargs):
        context = super(DetailSubjectView, self).get_context_data()
        subject = Subject.objects.get(pk=self.kwargs.get('pk'))
        context['owner'] = subject.teacher
        context['topics'] = subject.topics.all()
        context['breadcrumbs'] = self.get_breadcrumbs(subject)
        return context

    def get_breadcrumbs(self, subject):
        breadcrumbs = list()
        breadcrumbs.append(
            {"url": "/", "title": "Inicio", "tooltip": "Inicio"})
        breadcrumbs.append(
            {"url": reverse_lazy('detail_subject', kwargs={'pk': self.kwargs.get('pk')}), "title": subject.name,
             "tooltip": _("Asignatura")})
        return breadcrumbs


class ListSubjectView(LoginRequiredMixin, ListView):
    template_name = 'subject/subject_list.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        subjects = list(Subject.objects.filter(teacher=self.request.user.userProfile))
        for subject in subjects:
            subject.num_topics = len(subject.topics.all())
        return subjects

    def get_context_data(self, **kwargs):
        context = super(ListSubjectView, self).get_context_data()
        context['my_subjects'] = self.request.user.userProfile.my_subjects.all()
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context

    def get_breadcrumbs(self):
        breadcrumbs = list()
        breadcrumbs.append(
            {"url": "/", "title": "Inicio", "tooltip": "Inicio"})
        breadcrumbs.append(
            {"url": reverse_lazy('list_subjects'), "title": _("Lista de asignaturas"),
             "tooltip": _("Lista de asignaturas")})
        return breadcrumbs


class DeleteSubjectView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = "/"

    def get(self, request, *args, **kwargs):
        subject = Subject.objects.get(pk=self.kwargs.get('pk'))
        owner = subject.teacher.user
        if self.request.user == owner:
            get_object_or_404(Subject, pk=subject.pk).delete()
            return redirect(reverse_lazy('list_subjects'))
        else:
            return super(DeleteSubjectView, self).post(request, *args, **kwargs)


class UserRegisterSubject(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id_subject = self.kwargs.get('pk')
        subject = Subject.objects.get(pk=id_subject)
        subject.students.add(UserProfile.objects.get(pk=self.request.user.userProfile.id))
        # self.request.user.userProfile.my_subjects.add(Subject.objects.get(pk=id_subject))
        return reverse_lazy('detail_subject', kwargs=self.kwargs)


class UserUnregisterSubject(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id_subject = self.kwargs.get('pk')
        subject = Subject.objects.get(pk=id_subject)
        subject.students.remove(UserProfile.objects.get(pk=self.request.user.userProfile.id))
        # self.request.user.userProfile.my_subjects.add(Subject.objects.get(pk=id_subject))
        return reverse_lazy('detail_subject', kwargs=self.kwargs)


import_uploader = AjaxFileUploader()
