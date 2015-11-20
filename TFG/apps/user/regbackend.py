from registration.backends.default.views import RegistrationView
from .forms import UserProfileForm
from .models import UserProfile

class MyRegistrationView(RegistrationView):

    form_class = UserProfileForm

    def register(self, request, form_class):
        new_user = super(MyRegistrationView, self).register(request, form_class)
        user_profile = UserProfile()
        user_profile.user = new_user
        user_profile.field = form_class.cleaned_data['field']
        user_profile.save()
        return user_profile