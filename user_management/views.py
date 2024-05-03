from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile 


class ProfileUpdateView(LoginRequiredMixin, UpdateView): 
    model = Profile 
    fields = ['display_name', 'email']
    template_name = 'update_user_form.html'