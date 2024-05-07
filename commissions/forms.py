from django import forms
from django.forms.models import inlineformset_factory

from .models import Commission, Job, JobApplication

class CommissionForm(forms.ModelForm): 
    class Meta: 
        model = Commission
        fields = '__all__'

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['creator'].disabled = True


class JobApplicationForm(forms.ModelForm): 
    class Meta: 
        model = JobApplication
        fields = ['job','applicant']

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['applicant'].disabled = True 
 
JobFormset = inlineformset_factory(Commission, Job, fields='__all__')