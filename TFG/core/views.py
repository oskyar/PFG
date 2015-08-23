from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from TFG.accounts.forms import RegisterUserForm, LoginUser
from TFG.accounts.models import UserProfile


# Create your views here.
def index(request):
    # Si el usuario esta ya logueado, lo redireccionamos a index_view
    if request.user.is_authenticated():
        return render(request, 'index.html', context)

    mensaje = ''
    if request.method == 'POST':
        form_login = LoginUser()
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return render(request, 'index.html', context)
            else:
                form_login = LoginUser()
                # Redireccionar informando que la cuenta esta inactiva
                # Lo dejo como ejercicio al lector :)

        mensaje = 'Nombre de usuario o contraseña no valido'
    else:
        form_login = LoginUser()

    context = {'form_login': form_login, 'mensaje': mensaje}
    return render(request, 'index.html', context)


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
