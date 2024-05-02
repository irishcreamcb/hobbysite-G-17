from django.db import models
from django.urls import reverse 

from user_management.models import Profile


class Commission(models.Model): 
    title = models.CharField(max_length=255)
    description = models.TextField() 
    STATUS_CHOICES = [
        'Open', 
        'Full', 
        'Completed', 
        'Discontinued'
    ]
    status = models.CharField(choices=STATUS_CHOICES, 
                              default='Open',) 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
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
    STATUS_CHOICES = [
        'Open',
        'Full'
    ]
    status = models.CharField(choices=STATUS_CHOICES, 
                              default='Open',)

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
    STATUS_CHOICES = [
        'Pending', 
        'Accepted', 
        'Rejected', 
    ]
    status = models.CharField(choices=STATUS_CHOICES,
                              default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = [
            'status', 
            '-applied_on'
        ]