__author__ = 'oskyar'

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import UpdateView
from registration.backends.default.views import RegistrationView
from . import signals
from .forms import UserProfileForm
from .models import UserProfile
from guardian.shortcuts import assign_perm


class UserProfileView(RegistrationView):
    # template_name = 'user/register.html'
    disallowed_url = 'registration_disallowed'
    # http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = 'registration_complete'

    # success_url = reverse_lazy('thanks')
    form_class = UserProfileForm

    def register(self, form):
        new_user = super(UserProfileView, self).register(form)
        user_profile = UserProfile()
        user_profile.user = new_user
        user_profile.dni = form.cleaned_data['dni']
        user_profile.photo = form.cleaned_data['photo']
        user_profile.created_on = timezone.now()
        user_profile.modify_on = timezone.now()
        user_profile.save()
        assign_perm('user.change_user', self.request.user, user_profile)

        return user_profile

    def form_valid(self, form):
        # print("Form_valid")
        response = super(UserProfileView, self).form_valid(form)
        if self.request.is_ajax():
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super(UserProfileView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=200)
        else:
            return response

            # def get(self, request, *args, **kwargs):
            # super(UserProfile,self).get():


def myProfile(self, user, *args, **kwargs):
    return user.username == kwargs["pk"]


class UserProfileUpdateView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "user/edit_profile.html"
    context_object_name = 'form'
    success_url = "."
    success_message = _("Perfil actualizado satisfactoriamente")

    def test_func(self):
        return self.request.user.username == self.kwargs['pk']

    def get_object(self, queryset=None):
        # print (User.objects.get(username=self.kwargs["pk"]).id)
        # queryset=UserProfile.objects.get(user=User.objects.get(username=self.kwargs["pk"]).id)
        user = UserProfile.objects.get(user=User.objects.get(username=self.kwargs["pk"]).id)
        # print (user)

        return user

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(UserProfileUpdateView, self).get_initial()

        userProfile = UserProfile.objects.get(user=User.objects.get(username=self.kwargs["pk"]).id)
        initial['username'] = userProfile.user.username

        initial['first_name'] = userProfile.user.first_name
        initial['last_name'] = userProfile.user.last_name
        initial['email'] = userProfile.user.email
        initial['email2'] = userProfile.user.email
        initial['dni'] = userProfile.dni
        initial['photo'] = userProfile.photo
        return initial

    def form_valid(self, form):

        response = super(UserProfileUpdateView, self).form_valid(form)
        # Recuperamos el usuario y lo guardamos
        user = User.objects.get(pk=self.get_object().user.pk)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()
        # Recuperamos UserProfile para modificar la fecha de modificación
        userProfile = UserProfile.objects.get(pk=self.get_object().pk)
        userProfile.modify_on = timezone.now()
        userProfile.photo = form.cleaned_data['photo']
        userProfile.save()
        # messages.add_message(self.request, messages.SUCCESS, _("Perfil actualizado"))
        storage = messages.get_messages(self.request)
        storage.used = True

        signals.update_user_profile.send(sender=self.__class__,
                                         user=userProfile,
                                         request=self.request)

        return response

    def form_invalid(self, form):
        response = super(UserProfileUpdateView, self).form_invalid(form)
        print(form.errors)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=200)
        else:
            return response
