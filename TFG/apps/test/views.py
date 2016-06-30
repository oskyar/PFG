__author__ = 'oskyar'

from TFG.mixins import LoginRequiredMixin
from django.shortcuts import redirect
# from django.views.generic import CreateView
from vanilla import CreateView
from .forms import TestForm
from .models import Test
from TFG.apps.subject.models import Subject
from TFG.apps.topic.models import Topic
from guardian.shortcuts import assign_perm
from guardian.decorators import permission_required
from django.contrib.auth.models import User
from time import timezone

class CreateTestView(LoginRequiredMixin, CreateView):
    template_name = 'test/test_create.html'
    model = Test
    form_class = TestForm
    success_url = "/"

    def get_object(self):
        pass

    def get_context_data(self, **kwargs):
        context = super(CreateTestView, self).get_context_data(**kwargs)

        # context['topics'] = Topic.objects.filter(subject=subject)
        return context

    def form_valid(self, form):
        print("Valid")
        test = form.save(commit=False)
        test.owner = self.request.user.userProfile
        test.subject = Subject.objects.get(pk=self.kwargs['pk'])
        if test.type is Test.STANDARD:
            test.duration = None
        elif test.type is Test.CHRONO_TEST:
            test.duration = test.duration * 60  # Lo pasamos a segundos.

        if test.start_date and test.end_date and test.end_date < test.start_date:
            raise forms.ValidationError("La fecha de finalización no puede ser anterior a la de inicio",
                                        code="select_required")

        test.created_on = timezone.now()
        test.save()
        assign_perm('test.add_test', self.request.user, test)
        assign_perm('test.change_test', self.request.user, test)
        assign_perm('test.delete_test', self.request.user, test)

        assign_perm('test.add_test', test.subject.teacher.user, test)
        assign_perm('test.change_test', test.subject.teacher.user, test)
        assign_perm('test.delete_test', test.subject.teacher.user, test)

        # return redirect("create_topic", pk=self.kwargs['pk'])

        # return redirect("create_topic", pk=subject.id)
        return super(CreateTestView, self).form_valid(form)

    def form_invalid(self, form):
        print("Invalid")
        return super(CreateTestView, self).form_invalid(form)
