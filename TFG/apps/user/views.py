__author__ = 'oskyar'

from django.views.generic import TemplateView
from django.contrib.sites.shortcuts import get_current_site
from registration.backends.default.views import RegistrationView
from registration.models import RegistrationProfile
from registration import signals
from django.http import JsonResponse

from .forms import UserProfileForm
from .models import User, UserProfile
from datetime import datetime


class UserProfileView(RegistrationView):
    # template_name = 'user/register.html'
    # disallowed_url = 'registration_disallowed'
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
        user_profile.created_on = datetime.now()
        user_profile.modify_on = datetime.now()
        user_profile.save()

        return user_profile

    def form_valid(self, form):
        print("Entra en valid")

        # print("Form_valid")
        response = super(UserProfileView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):

        # print(self)
        print("Formulario invalido")
        response = super(UserProfileView, self).form_invalid(form)
        print(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=200)
        else:
            return response

    def check_username(self, form):
        print(UserProfile.objects.get_user_by_username(form.cleaned_data['username']))


data = {
    'username': 'pepito',
    'first_name': 'pepito',
    'last_name': 'pepito',
    'email': 'pepito@email.com',
    'password1': '123123',
    'password2': '123123'
}
