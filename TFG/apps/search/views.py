__author__ = 'oskyar'

from TFG.apps.answer.forms import InlineAnswerFormSet, AnswerInline
from TFG.apps.topic.models import Topic, Subtopic
from TFG.apps.subject.models import Subject
from TFG.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from vanilla import CreateView, TemplateView, RedirectView, ListView
from django.shortcuts import redirect


class SearchView(ListView):
    template_name = "search/search.html"
    context_object_name = "subjects"

    def get_queryset(self):
        return Subject.objects.filter(name__icontains=self.kwargs.get('search')).exclude(
            teacher__user_id=self.request.user.id).exclude(students__exact=self.request.user.userProfile)

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data()
        context['breadcrumbs'] = self.get_breadcrumbs()
        context['subjects_owner'] = self.request.user.userProfile.subjects.all()
        context['my_subjects'] = self.request.user.userProfile.my_subjects.all()
        context['token'] = self.kwargs['search']
        context['last_subjects'] = Subject.objects.all().order_by('created_on')[:10]
        return context

    def get(self, request, *args, **kwargs):
        # return redirect('search', kwargs=kwargs)
        return super(SearchView, self).get(request, args, kwargs)

    def get_breadcrumbs(self):
        breadcrumbs = list()
        breadcrumbs.append(
            {"url": "/", "title": "Inicio", "tooltip": "Inicio"})
        breadcrumbs.append(
            {"url": "#",
             "title": _("Buscador"),
             "tooltip": _("Buscador de asignaturas por nombre y autor")})

        return breadcrumbs
