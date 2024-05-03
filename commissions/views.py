from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Commission, Job


class CommissionListView(ListView): 
    model = Commission 
    template_name = 'commission_list.html'


class CommissionDetailView(DetailView): 
    model = Commission 
    template_name = 'commission_detail.html'


class CommissionCreateView(CreateView): 
    model = Commission
    template_name = 'commission_form.html' 

    def __init__(self, *args, creator, **kwargs): #yoinked from https://forum.djangoproject.com/t/best-way-to-use-a-created-by-type-field/3067
        super().__init__(*args, **kwargs)
        self.creator = creator

    def save(self, *args, **kwargs):
        self.instance.creator = self.creator
        return super().save(*args, **kwargs)