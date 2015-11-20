__author__ = 'oskyar'

from django.contrib.auth.forms import forms


class LoginUser(forms.Form):
    username = forms.CharField(
        min_length=5,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'id': 'usernameLogin'}),
        label="Usuario")

    password = forms.CharField(
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}),
        label="Contraseña")

