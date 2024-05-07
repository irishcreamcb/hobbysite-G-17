from django import forms
from django.forms.models import inlineformset_factory

from .models import Commission, Job, JobApplication

JobFormset = inlineformset_factory(Commission, Job, fields='__all__')