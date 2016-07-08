__author__ = 'oskyar'

from TFG.mixins import LoginRequiredMixin
# from django.views.generic import CreateView
from vanilla import CreateView, TemplateView, RedirectView
from .forms import TestForm
from .models import Test, TestDone
from TFG.apps.subject.models import Subject
from TFG.apps.question.models import Question
from TFG.apps.answer.models import Answer
from TFG.apps.topic.models import Topic, Subtopic
from TFG.apps.statistic.models import StatisticQuestion
from TFG.apps.user.models import UserProfile
from TFG.apps.user.views import get_level, get_min_max
from guardian.shortcuts import assign_perm
from django import forms
import uuid
from guardian.shortcuts import get_perms
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
import random
from django.http import JsonResponse
import json
from django.utils.timezone import now
from ipware.ip import get_real_ip


class CreateTestView(LoginRequiredMixin, CreateView):
    template_name = 'test/test_create.html'
    model = Test
    form_class = TestForm
    success_url = "/"

    def get_object(self):
        pass

    def get_form(self, data=None, files=None, **kwargs):
        form = super(CreateTestView, self).get_form(data, files, **kwargs)
        form.fields['owner'].initial = self.request.user.userProfile
        form.fields['owner'].widget = forms.HiddenInput()
        form.fields['activation_code'].initial = uuid.uuid4().hex[:6].upper()
        form.fields['autogenerate_questions'].required = False
        form.fields['question'].required = False
        if 'pk' in self.kwargs:
            subject = Subject.objects.get(pk=self.kwargs.get('pk'))
            if 'change_subject' in get_perms(self.request.user, subject):
                form.fields['subject'].initial = subject
                form.fields['subject'].widget = forms.HiddenInput()
            elif 'unregister_subject' in get_perms(self.request.user, subject):
                form.fields['subject'] = forms.ChoiceField(
                    choices=[(o.id, str(o)) for o in
                             Subject.objects.filter(students__exact=self.request.user.userProfile)])
                # form.fields['subject'].widget = forms.HiddenInput()

                # form.fields['subject'].choices = dict({subject.name, subject.id})

        return form

    def get_context_data(self, **kwargs):
        context = super(CreateTestView, self).get_context_data(**kwargs)
        if ('pk' in self.kwargs):
            context['subject'] = Subject.objects.get(pk=self.kwargs.get('pk'))
        # context['topics'] = Topic.objects.filter(subject=subject)
        return context

    def form_valid(self, form):
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

        test.created_on = now()
        test.save()
        if self.request.user != test.subject.teacher.user:
            assign_perm('add_test', self.request.user, test)
            assign_perm('change_test', self.request.user, test)
            assign_perm('delete_test', self.request.user, test)

        assign_perm('add_test', test.subject.teacher.user, test)
        assign_perm('change_test', test.subject.teacher.user, test)
        assign_perm('delete_test', test.subject.teacher.user, test)

        # return redirect("create_topic", pk=self.kwargs['pk'])

        return redirect("detail_subject", pk=subject.id)
        # return super(CreateTestView, self).form_valid(form)

    def form_invalid(self, form):
        print("Invalid")
        return super(CreateTestView, self).form_invalid(form)


class DoTestView(LoginRequiredMixin, CreateView):
    template_name = 'test/do_test.html'
    model = Test
    form_class = TestForm
    success_url = "/"
    fields = ['owner', 'subject', 'subtopic', 'topic', 'name', 'type', 'num_question', 'type_question']

    def get_form(self, data=None, files=None, **kwargs):
        form = super(DoTestView, self).get_form(data, files, **kwargs)
        subject = Subject.objects.get(pk=self.kwargs.get('pk'))
        form.fields['visibility'].initial = Test.PRIVATE
        form.fields['subject'] = forms.ModelChoiceField(
            queryset=Subject.objects.filter(students__exact=self.request.user.userProfile))
        form.fields['subject'].initial = subject
        # form.fields['subject'].disabled = True
        # form.fields['subject'].required = True
        # form.fields['owner'].required = False
        form.fields['visibility'].required = False
        form.fields['autogenerate_questions'].required = False
        form.fields['question'].required = False
        form.fields['subject'].widget = forms.HiddenInput()
        form.fields['owner'] = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user=self.request.user))
        form.fields['owner'].initial = self.request.user.userProfile
        form.fields['owner'].widget = forms.HiddenInput()
        form.fields['name'].initial = "Test nº " + str(
            Test.objects.filter(owner=self.request.user.userProfile).count() + 1)
        return form

    def get_context_data(self, **kwargs):

        context = super(DoTestView, self).get_context_data(**kwargs)
        if ('pk' in self.kwargs):
            context['subject'] = Subject.objects.get(pk=self.kwargs.get('pk'))
        # context['topics'] = Topic.objects.filter(subject=subject)
        return context

    def form_valid(self, form):
        test = form.save(commit=False)
        test.owner = self.request.user.userProfile
        test.autogenerate_questions = True
        questions = None
        if 'pk' in self.kwargs:
            subject = Subject.objects.get(pk=self.kwargs.get('pk'))
            test.subject = subject
        if test.subtopic:
            num_question_available = Subtopic.objects.get_num_questions(test.subtopic, test.type_question)
            if test.num_question > num_question_available:
                messages.error(self.request, "Error: %s(%s) %s(%d)" % (
                    _("El número de preguntas disponibles "), num_question_available,
                    _(" es menor que el número de preguntas que ha indicado"), test.num_question))
                return redirect(reverse_lazy('do_test', kwargs=self.kwargs))
            questions = Subtopic.objects.get_all_questions(test.subtopic, test.type_question)
        elif test.topic:
            num_question_available = Topic.objects.get_num_questions(test.topic, test.type_question)
            if test.num_question > num_question_available:
                messages.error(self.request, "Error: %s(%s) %s(%d)" % (
                    _("El número de preguntas disponibles "), num_question_available,
                    _(" es menor que el número de preguntas que ha indicado"), test.num_question))

                return redirect(reverse_lazy('do_test', kwargs=self.kwargs))
            questions = Topic.objects.get_all_questions(test.topic, test.type_question)
        elif test.subject:
            num_question_available = Subject.objects.get_num_questions(subject, test.type_question)
            if test.num_question > num_question_available:
                # messages.add_message(self.request, messages.SUCCESS, _("Perfil actualizado"))

                messages.error(self.request, "Error: %s(%s) %s(%d)" % (
                    _("El número de preguntas disponibles "), num_question_available,
                    _(" es menor que el número de preguntas que ha indicado"), test.num_question))

                return redirect(reverse_lazy('do_test', kwargs=self.kwargs))
            questions = Subject.objects.get_all_questions(test.subject, test.type_question)

        random_question = disarray_questions(questions, test.num_question)

        test.owner = self.request.user.userProfile
        test.subject = Subject.objects.get(pk=self.kwargs['pk'])
        if test.type is Test.STANDARD:
            test.duration = None
        elif test.type is Test.CHRONO_TEST:
            test.duration = test.duration * 60  # Lo pasamos a segundos.

        test.created_on = now()
        test.save()

        for x in range(len(random_question)):
            random_question[x].tests.add(test)
            # test.questions.add(random_question[x])
        # [test.questions.add(random_question[x]) for x in range(len(random_question))]
        if self.request.user != test.subject.teacher.user:
            assign_perm('add_test', self.request.user, test)
            assign_perm('change_test', self.request.user, test)
            assign_perm('delete_test', self.request.user, test)

        assign_perm('add_test', test.subject.teacher.user, test)
        assign_perm('change_test', test.subject.teacher.user, test)
        assign_perm('delete_test', test.subject.teacher.user, test)

        # return redirect("create_topic", pk=self.kwargs['pk'])

        # return redirect("create_topic", pk=subject.id)
        self.kwargs['pk_test'] = test.pk

        return redirect(reverse_lazy('doing_test', kwargs=self.kwargs))

    def form_invalid(self, form):
        print("Invalid")
        return super(DoTestView, self).form_invalid(form)


def disarray_questions(questions, num_question_test):
    if len(questions) > num_question_test:
        return random.sample(questions, num_question_test)
    else:
        return random.sample(questions, len(questions))


class DoTestRedirectDoingTest(RedirectView):
    def get(self, request, *args, **kwargs):
        test = Test()
        test.owner = self.request.user.userProfile
        subtopic = Subtopic.objects.get(pk=self.kwargs.get('pk_subtopic'))
        test.subtopic = subtopic
        test.topic = subtopic.topic
        test.subject = subtopic.topic.subject
        test.gamificado = True
        test.num_question = subtopic.num_questions_gami
        test.active = True
        test.autogenerate_questions = True
        test.created_on = now()
        test.name = "%s %d" % ("Test gamificado nº", test.testsdone.filter(
            student__user=self.request.user).count() + 1)
        test.save()
        questions = Subtopic.objects.get_all_questions(subtopic, test.type_question)

        random_question = disarray_questions(questions, test.num_question)

        for x in range(len(random_question)):
            random_question[x].tests.add(test)

        return redirect(reverse_lazy('doing_test', kwargs={'pk': subtopic.topic.subject.id, 'pk_test': test.id}))


class DoingTestView(TemplateView):
    template_name = "test/doing_test.html"

    def get_context_data(self, **kwargs):
        context = super(DoingTestView, self).get_context_data(**kwargs)
        context['subject'] = Subject.objects.get(pk=self.kwargs.get('pk'))
        context['test'] = Test.objects.get(pk=self.kwargs.get('pk_test'))
        return context

    def get_queryset(self):
        return


class DoneTestView(CreateView):
    template_name = "test/done_test.html"
    model = TestDone
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        test = Test.objects.get(pk=kwargs.get('pk_test'))
        num_questions = test.question.all().count()
        num_replies_valids = 0
        num_replies_invalids = 0
        num_replies_no_answered = 0
        correct_replies = list()
        replies = json.loads(request.body.decode("utf-8"))
        for i in range(1, num_questions + 1):
            reply = replies.get('reply_' + str(i))
            num_answer = reply.get('answer_id')

            if num_answer:
                answer = Answer.objects.get(pk=num_answer)
                if answer and answer.valid:
                    statistic = StatisticQuestion.objects.get_or_create(question=answer.question)
                    statistic[0].num_generated += 1
                    statistic[0].num_answered += 1
                    statistic[0].num_successful += 1
                    num_replies_valids += 1
                    statistic[0].save()
                    correct_replies.append('answer_' + num_answer)
                elif answer:
                    answer_correct = answer.question.answer.filter(valid__exact=True)
                    for a in answer_correct:
                        correct_replies.append('answer_' + str(a.id))
                    num_replies_invalids += 1

            else:
                question = Question.objects.get(pk=reply.get('question_id'))
                statistic = StatisticQuestion.objects.get_or_create(question=question)
                num_replies_no_answered += 1
                # num_replies_invalids += 1
                statistic[0].num_generated += 1
                statistic[0].save()

        testDone = TestDone()
        testDone.student = self.request.user.userProfile
        testDone.test = test
        testDone.realization_date = now()
        testDone.IP = get_real_ip(self.request)
        over_10 = 10 * num_replies_valids / (num_replies_invalids + num_replies_valids)
        testDone.result = over_10
        if num_replies_valids >= num_replies_invalids:
            testDone.passed = True
            text_pass = _("Aprobado")
        else:
            testDone.passed = False
            text_pass = _("No pasado")
        testDone.replies = replies
        percent = num_replies_valids / (num_replies_valids + num_replies_invalids + num_replies_no_answered) * 100

        total_score = 0
        total_score += num_replies_valids
        total_score += 5 if testDone.passed == True else 0
        total_score += 10 if percent == 100 and testDone.test.question.count() >= 10 else 0
        total_score -= 0.5 * num_replies_invalids
        total_score -= testDone.test.question.count() / 2 if percent < 20 else 0
        self.request.user.userProfile.score += total_score

        self.request.user.userProfile.level = get_level(self.request.user.userProfile.score)
        (self.request.user.userProfile.prev_level, self.request.user.userProfile.next_level) = get_min_max(
            self.request.user.userProfile.score)
        self.request.user.userProfile.save()

        testDone.score_won = total_score
        testDone.percent = percent
        testDone.save()

        result = {'pass': testDone.passed, 'text_pass': text_pass, 'valids': num_replies_valids,
                  'invalids': num_replies_invalids + num_replies_no_answered,
                  'percent': percent, 'over_10': over_10, 'correct_replies': correct_replies,
                  'total_score': total_score}
        return JsonResponse(result)
