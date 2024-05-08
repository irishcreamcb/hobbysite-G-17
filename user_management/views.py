from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile 


class ProfileUpdateView(LoginRequiredMixin, UpdateView): 
    model = Profile 
    fields = ['display_name', 'email']
    template_name = 'user_management/update_user_form.html'
    
    def get_object(self):
        obj = super().get_object()
        obj = Profile.objects.get(user__pk=obj.pk)
        obj.save()
        return obj

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        return form