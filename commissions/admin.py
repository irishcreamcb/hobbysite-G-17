from django.contrib import admin
from .models import Commission, Job 


class CommissionInline(admin.TabularInline): 
    model = Commission


class JobInline(admin.TabularInline): 
    model = Job


class CommissionAdmin(admin.ModelAdmin): 
    model = Commission
    inlines = [JobInline,]

    list_display = ['title']


admin.site.register(Commission, CommissionAdmin)