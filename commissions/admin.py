from django.contrib import admin
from .models import Commission, Job, JobApplication


class CommissionInline(admin.TabularInline): 
    model = Commission


class JobInline(admin.TabularInline): 
    model = Job


class JobApplicationInline(admin.TabularInline):
    model = JobApplication


class CommissionAdmin(admin.ModelAdmin): 
    model = Commission
    inlines = [JobInline,]

    list_display = ['title']


class JobAdmin(admin.ModelAdmin): 
    model = Job
    inlines = [JobApplicationInline,] 

    list_display = ['role']


admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)