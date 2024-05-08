from django.db import models
from django.urls import reverse 
from django.db.models import Sum

from user_management.models import Profile


class Commission(models.Model): 
    title = models.CharField(max_length=255)
    description = models.TextField() 
    STATUS_CHOICES = {
        'O' : 'Open', 
        'F' : 'Full', 
        'C' : 'Completed', 
        'D' : 'Discontinued'
    }
    status = models.CharField(choices=STATUS_CHOICES, 
                              default='O',
                              max_length=2) 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(Profile, 
                                on_delete=models.CASCADE,
                                related_name='commission',)
    
    class Meta: 
        ordering = [
            'status',
            'created_on',
        ] 

    def __str__(self): 
        return self.title
    
    def get_absolute_url(self): 
        return reverse('commissions:commission-detail', args=[self.pk])


class Job(models.Model): 
    commission = models.ForeignKey(Commission,
                                   on_delete=models.CASCADE, 
                                   related_name='jobs',)
    role = models.CharField(max_length=255)
    manpower_required = models.IntegerField()
    STATUS_CHOICES = {
        'O' : 'Open',
        'F' : 'Full'
    }
    status = models.CharField(choices=STATUS_CHOICES, 
                              default='O',
                              max_length=2)

    class Meta: 
        ordering = [
            'status', 
            '-manpower_required',
            'role'
        ]

    def __str__(self): 
        return self.role
    

class JobApplication(models.Model): 
    job = models.ForeignKey(Job,
                            on_delete=models.CASCADE, 
                            related_name='applications',)
    applicant = models.ForeignKey(Profile,
                                  on_delete=models.CASCADE, 
                                  related_name='commission_job')
    STATUS_CHOICES = {
        'P' : 'Pending', 
        'A' : 'Accepted', 
        'R' : 'Rejected', 
    }
    status = models.CharField(choices=STATUS_CHOICES,
                              default='P',
                              max_length=2)
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = [
            'status', 
            '-applied_on'
        ]