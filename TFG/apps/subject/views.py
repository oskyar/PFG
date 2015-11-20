__author__ = 'oskyar'

from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse_lazy
from .models import UserProfile

from .forms import RegisterUserForm


class RegisterUser(FormView):
    template_name = 'user/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        user = form.save()
        profile = UserProfile()
        profile.user = user
        #profile.photo = form.cleaned_data['photo']
        #profile.save()
        return super(RegisterUser, self).form_valid(form)


class ThanksView(TemplateView):
    template_name = 'user/thanks.html'
    #return render(request, 'thanks.html', {'username': username})
