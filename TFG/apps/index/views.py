from django.shortcuts import render


from django.views.generic import TemplateView
from .forms import LoginUser

# Create your views here.
class Index(TemplateView):
    template_name = "index/index.html"
    #model = LoginUser
    #def get(self, request, *args, **kwargs):
    #    context_dict = {'form_login' : LoginUser()}
    #    render(request, template_name, context_dict)