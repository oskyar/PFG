__author__ = 'oskyar'

from TFG.apps.user.models import UserProfile
from TFG.decorators import cbv_permission_required_or_403
# from TFG.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from guardian.shortcuts import assign_perm, remove_perm, get_perms
from vanilla import DetailView, RedirectView, UpdateView, DeleteView, ListView, CreateView, TemplateView
from .forms import CreateSubjectForm
from .models import Subject
from django.contrib import messages
from TFG.apps.test.models import Test, TestDone
from TFG.apps.topic.models import Topic, Subtopic
from django.db.models import Sum, Avg
from django.core.mail import send_mass_mail, EmailMessage
from django.core import mail


@cbv_permission_required_or_403('add_subject')
class CreateSubjectView(LoginRequiredMixin, CreateView):
    template_name = 'subject/subject_create.html'
    form_class = CreateSubjectForm
    success_url = "/"
    login_url = reverse_lazy('login')

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
        # assign_perm('subject.add_subject', self.request.user, subject)
        assign_perm('change_subject', self.request.user, subject)
        assign_perm('delete_subject', self.request.user, subject)
        remove_perm('register_subject', self.request.user, subject)

        # return redirect("/subject/"+str(subject.id)+"/topic/create")

        # return redirect("create_topic", pk=subject.id)
        return super(CreateSubjectView, self).form_valid(form)

    def form_invalid(self, form):
        return super(CreateSubjectView, self).form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        self.token = csrf_token
        return super(CreateSubjectView, self).dispatch(request, *args,
                                                       **kwargs)

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


@cbv_permission_required_or_403('change_subject', (Subject, 'pk', 'pk'))
class UpdateSubjectView(LoginRequiredMixin, UpdateView):
    form_class = CreateSubjectForm
    fields = "__all__"
    template_name = "subject/subject_create.html"
    context_object_name = 'subject'
    lookup_field = 'pk'

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
        if "edit_subject" in self.request.POST:
            messages.success(self.request, _("Asignatura actualizada correctamente"))
            return reverse_lazy("edit_subject", kwargs={'pk': self.object.id})
        else:
            messages.success(self.request, _("La asignatura actualizada correctamente, puedes seguir creando temas."))
            return reverse_lazy("create_topic", kwargs={'pk': self.object.id})


class DetailSubjectView(DetailView):
    model = Subject
    template_name = "subject/subject_detail.html"
    lookup_field = 'pk'

    def get_context_data(self, **kwargs):
        context = super(DetailSubjectView, self).get_context_data()
        subject = Subject.objects.get(pk=self.kwargs.get('pk'))
        context['owner'] = subject.teacher
        topics_gamificados = list(subject.topics.filter(gamificar=True))
        context['breadcrumbs'] = self.get_breadcrumbs(subject)
        context['tests_done'] = self.request.user.userProfile.testsdone.test_gamificados(subject)

        prev_passed = True
        prev_topic = True
        subtopic_pass = 0
        pass_topic = False
        for topic in topics_gamificados:
            topic.subtopics_gamificados = topic.subtopics.filter(gamificar=True)
            topic.prev_topic = prev_topic
            for subtopic in topic.subtopics_gamificados:
                subtopic.testsdone = TestDone.objects.filter(student=self.request.user.userProfile,
                                                             test__subtopic=subtopic)
                subtopic.prev_passed = prev_passed
                if TestDone.objects.filter(student=self.request.user.userProfile, test__subtopic=subtopic,
                                           passed=True).count() > 0:
                    prev_passed = True
                    subtopic_pass += 1
                    # subtopic.passed = True
                else:
                    if prev_passed == True:
                        subtopic_pass += 1
                    prev_passed = False
                    # subtopic.passed = False
            if subtopic_pass == len(topics_gamificados):
                prev_topic = True
                topic.passed = True
            else:
                prev_topic = False
                topic.passed = False

        context['topics'] = topics_gamificados

        my_students = list(subject.students.all())
        for student in my_students:
            student.score_subject = TestDone.objects.filter(student=student, test__subject=subject).aggregate(
                Sum('score_won'))['score_won__sum']
            student.average = TestDone.objects.filter(student=student, test__subject=subject).aggregate(
                Avg('percent'))['percent__avg']
            student.num_test_done = TestDone.objects.filter(student=student, test__subject=subject).count()
        subject.students.order_by('score_subject')

        context['clasification'] = my_students

        # subtopics_gamificados = list(Subtopic.objects.filter(gamificar=True, topic__gamificar=True, topic__subject=subject))
        # topic_gamificados = subject.topics.filter(gamificar=True)
        # subtopics_gamificados = [topic.subtopics.filter(gamificar=True) for topic in topic_gamificados]
        # subtopics_gam_testdone = [subtopic for subtopic in subtopics_gamificados if subtopic.topic.subject.tests.filter(testsdone__passed=True)]
        if 'change_test' in get_perms(self.request.user, subject):
            owner = subject.teacher
        else:
            owner = self.request.user.userProfile
        context['tests_generales'] = Test.objects.without_gamificar_by_owner(subject, owner)
        context['tests_done'] = Test.objects.without_gamificar_by_owner(subject, self.request.user.userProfile)
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


@cbv_permission_required_or_403('delete_subject', (Subject, 'pk', 'pk'))
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
        if subject.students.all().count() + 1 < subject.capacity:
            subject.students.add(UserProfile.objects.get(pk=self.request.user.userProfile.id))
        else:
            messages.error(self.request, "%s(%d), %s" % (_(
                "No ha sido posible matricularse a la asignatura debido a que está llena, por favor contacte con su profesor"),
                                                         subject.name, subject.teacher.user.first_name))
            return redirect(reverse_lazy('do_test', kwargs=self.kwargs))
        assign_perm('unregister_subject', self.request.user, subject)
        # self.request.user.userProfile.my_subjects.add(Subject.objects.get(pk=id_subject))
        return reverse_lazy('detail_subject', kwargs=self.kwargs)


class UserUnregisterSubject(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id_subject = self.kwargs.get('pk')
        subject = Subject.objects.get(pk=id_subject)
        subject.students.remove(UserProfile.objects.get(pk=self.request.user.userProfile.id))
        remove_perm('unregister_subject', self.request.user, subject)
        # self.request.user.userProfile.my_subjects.add(Subject.objects.get(pk=id_subject))
        return reverse_lazy('detail_subject', kwargs=self.kwargs)


@cbv_permission_required_or_403('change_subject', (Subject, 'pk', 'pk'))
class SendTestSubjectView(LoginRequiredMixin, TemplateView):
    template_name = "/"

    def get(self, request, *args, **kwargs):
        subject = Subject.objects.get(pk=self.kwargs.get('pk'))
        test = Test.objects.get(pk=self.kwargs.pop('pk_test'))
        list_emails = [student.user.email for student in subject.students.all()]

        message1 = (
            'Test NUEVO: ' + test.name + " de la asignatura " + subject.name,
            '¡¡Hay un nuevo test para realizar en la plataforma, accede a ahora para realizarlo!!',
            'test.tfg.zafra@gmail.com',
            list_emails)
        send_mass_mail((message1, message1), fail_silently=False)

        # get_object_or_404(Subject, pk=subject.pk).delete()
        messages.success(self.request, "Test enviado correctamente a los alumnos")

        return redirect(reverse_lazy('detail_subject', kwargs=self.kwargs))
