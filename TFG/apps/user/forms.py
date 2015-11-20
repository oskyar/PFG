from django.contrib.auth.views import password_change

__author__ = 'oskyar'

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.utils.translation import ugettext_lazy as _


class RegisterUserForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    username = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'id': 'usernameRegister'}),
        label="*Usuario:")

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'mdl-textfield__input'}),
        label="*Email:")

    first_name = forms.CharField(
        min_length=2,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
        label="*Nombre:")

    last_name = forms.CharField(
        min_length=2,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
        label="Segundo nombre:")

    password1 = forms.CharField(
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}),
        label="*Contraseña:")

    password2 = forms.CharField(
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}),
        label="*Repita contraseña:",
        help_text=_("Enter the same password as above, for verification."))


    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

        #
        # photo = forms.ImageField(
        #     required=False,
        #     label="")

    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return email

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2
