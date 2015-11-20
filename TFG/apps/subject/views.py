__author__ = 'oskyar'

from TFG.mixins import LoginRequiredMixin
from ajaxuploader.views import AjaxFileUploader
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView
from .forms import CreateSubjectForm
from .models import Subject
from registration.models import RegistrationProfile


class CreateSubjectView(LoginRequiredMixin, CreateView):
    template_name = 'subject/create.html'
    form_class = CreateSubjectForm
    success_url = "/"

    def form_valid(self, form):
        sb = form.cleaned_data
        print(self.request.user.id)
        teacher = RegistrationProfile.objects.get(pk=self.request.user.id)
        print (teacher)
        subject = Subject.objects.create(
            teacher=teacher,
            name=sb['name'],
            description=sb['description'],
            category="prueba",
            test_opt=sb['test_opt'],
            capacity=sb['capacity'],
            image=sb['image']
        )
        # subject.teacher = RegistrationProfile.objects.get(uid)
        # print(subject.teacher)

        

        # profile.photo = form.cleaned_data['photo']
        # profile.save()
        return super(CreateSubjectView, self).form_valid(form)
    
    def form_invalid(self, form):
        print ("Formulario invalido")
        print (form)
        return super(CreateSubjectView, self).form_invalid(form)
    
    # @method_decorator(csrf_except)

    def dispatch(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        self.token = csrf_token
        return super(CreateSubjectView, self).dispatch(request, *args,
                                                       **kwargs)  # Método que sirve para la inserción de imágenes por medio de Ajax


def start(request):
    return render_to_response('import.html',
                              {'csrf_token': csrf_token}, context_instance=RequestContext(request))


import_uploader = AjaxFileUploader()
