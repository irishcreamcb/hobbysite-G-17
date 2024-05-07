from typing import Any
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Commission, JobApplication, Job
from .forms import JobFormset, CommissionForm, JobApplicationForm


class CommissionListView(ListView): 
    model = Commission 
    template_name = 'commission_list.html'


class CommissionDetailView(DetailView): 
    model = Commission 
    template_name = 'commission_detail.html'

    def get_context_data(self, **kwargs): 
        self.object = self.get_object()
        comm = self.object
        jobs = Job.objects.filter(commission=comm)
        total_manpower = 0
        difference = 0 
        for x in jobs: 
            total_manpower += x.manpower_required
            applications = JobApplication.objects.filter(job=x)
            for i in applications: 
                difference += 1
        ctx = super().get_context_data(**kwargs)
        ctx['manpower'] = total_manpower
        ctx['remaining'] = total_manpower - difference 
        return ctx 


class CommissionCreateView(CreateView, LoginRequiredMixin): #yoinked from: https://swapps.com/blog/working-with-nested-forms-with-django/
    model = Commission
    template_name = 'commission_form.html' 
    form_class = CommissionForm

    def get_context_data(self, **kwargs): 
        data = super().get_context_data(**kwargs)
        if self.request.POST: 
            data['Jobs'] = JobFormset(self.request.POST)
        else: 
            data['Jobs'] = JobFormset()
        return data 
    
    def form_valid(self, form): 
        context = self.get_context_data() 
        jobs = context['Jobs']
        self.object = form.save() 
        if jobs.is_valid(): 
            jobs.instance = self.object 
            jobs.save() 
        return super().form_valid(form) 
    
    def get_initial(self):
        initial = super().get_initial()
        initial['creator'] = self.request.user.profile
        return initial
    
    def get_success_url(self):
        return reverse('commissions:commission-list')
    

class CommissionUpdateView(UpdateView, LoginRequiredMixin): 
    model = Commission
    template_name = 'commission_form.html' 
    fields = '__all__'

    def get_context_data(self, **kwargs): 
        data = super().get_context_data(**kwargs)
        if self.request.POST: 
            data['Jobs'] = JobFormset(self.request.POST, instance=self.object)
        else: 
            data['Jobs'] = JobFormset(instance=self.object)
        return data 
    
    def form_valid(self, form): 
        context = self.get_context_data() 
        jobs = context['Jobs']
        self.object = form.save() 
        if jobs.is_valid(): 
            jobs.instance = self.object 
            jobs.save() 
        return super().form_valid(form) 
    
    def get_success_url(self):
        return reverse('commissions:commission-list')


class JobApplicationCreateView(CreateView, LoginRequiredMixin): 
    model = JobApplication
    template_name = 'job_application.html'
    form_class = JobApplicationForm

    def get_initial(self):
        initial = super().get_initial()
        initial['applicant'] = self.request.user.profile
        return initial

    def get_success_url(self):
        return reverse('commissions:commission-list')