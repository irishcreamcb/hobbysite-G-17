from typing import Any
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Commission, JobApplication, Job
from .forms import JobFormset, CommissionForm, JobApplicationForm

from user_management.models import Profile


class CommissionListView(ListView): 
    model = Commission 
    template_name = 'commissions/commission_list.html'

    def get_context_data(self, **kwargs): 
        ctx = super().get_context_data(**kwargs)
        job_applications = [] 
        applied_by_user = [] 

        if self.request.user.is_authenticated: 
            user = Profile.objects.get(user=self.request.user)
            job_applications = JobApplication.objects.filter(applicant=user)

            for application in job_applications: 
                job = application.job
                commission = job.commission 
                if commission not in applied_by_user: 
                    applied_by_user.append(commission) 
                
        ctx['applications'] = job_applications
        ctx['applied_by_user'] = applied_by_user

        return ctx


class CommissionDetailView(DetailView): 
    model = Commission 
    template_name = 'commissions/commission_detail.html'

    def get_context_data(self, **kwargs): 
        self.object = self.get_object()
        comm = self.object
        jobs = Job.objects.filter(commission=comm)
        total_manpower = 0
        difference = 0 

        for x in jobs:  
            total_manpower += x.manpower_required
            job_taken = 0 
            applications = JobApplication.objects.filter(job=x)
            for i in applications: 
                if i.status == 'A':
                    difference += 1
                    job_taken += 1 
            if job_taken == x.manpower_required: 
                x.status = 'F' 
                x.save()  

        ctx = super().get_context_data(**kwargs)

        ctx['manpower'] = total_manpower
        ctx['remaining'] = total_manpower - difference 

        return ctx 


class CommissionCreateView(CreateView, LoginRequiredMixin): #yoinked from: https://swapps.com/blog/working-with-nested-forms-with-django/
    model = Commission
    template_name = 'commissions/commission_form.html' 
    form_class = CommissionForm

    def get_context_data(self, **kwargs): 
        data = super().get_context_data(**kwargs)

        if self.request.POST: 
            data['Jobs'] = JobFormset(self.request.POST)
        else: 
            data['Jobs'] = JobFormset()
        for form in data['Jobs']:
            for field in form.fields.values():
                if (field.widget.input_type == 'checkbox'):
                    field.widget.attrs.update({'class': 'form-check-input'})
                else:
                    field.widget.attrs.update({'class': 'form-control'})

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
    
    def get_form(self, form_class=form_class):
        form = super().get_form(form_class)

        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        return form
    
    def get_success_url(self):
        return reverse('commissions:commission-list')
    

class CommissionUpdateView(UpdateView, LoginRequiredMixin): 
    model = Commission
    template_name = 'commissions/commission_update.html' 
    form_class = CommissionForm

    def get_context_data(self, **kwargs): 
        data = super().get_context_data(**kwargs)

        if self.request.POST: 
            data['Jobs'] = JobFormset(self.request.POST, instance=self.object)
        else: 
            data['Jobs'] = JobFormset(instance=self.object)
        
        for form in data['Jobs']:
            for field in form.fields.values():
                if (field.widget.input_type == 'checkbox'):
                    field.widget.attrs.update({'class': 'form-check-input'})
                else:
                    field.widget.attrs.update({'class': 'form-control'})

        return data 
    
    def get_initial(self): 
        initial = super().get_initial()

        job_count = 0 
        full = 0 
        comm = Commission.objects.get(pk=self.get_object().pk)  
        job_list = Job.objects.filter(commission=comm)

        for x in job_list: 
            if x.status == 'F': 
                full += 1
            job_count += 1

        if full == job_count: 
            initial['status'] = 'F'

        return initial

    def form_valid(self, form): 
        context = self.get_context_data() 
        jobs = context['Jobs']
  
        self.object = form.save()

        if jobs.is_valid(): 
            jobs.instance = self.object 
            jobs.save()
        return super().form_valid(form) 
    
    def get_form(self, form_class=form_class):
        form = super().get_form(form_class)

        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        return form
    
    def get_success_url(self):
        return reverse('commissions:commission-list')


class JobApplicationCreateView(CreateView, LoginRequiredMixin): 
    model = JobApplication
    template_name = 'commissions/job_application.html'
    form_class = JobApplicationForm

    def get_initial(self):
        initial = super().get_initial()
        initial['applicant'] = self.request.user.profile
        
        return initial

    def get_form(self, form_class=form_class):
        form = super().get_form(form_class)

        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        return form

    def get_success_url(self):
        return reverse('commissions:commission-list')