from django import forms
from django.forms import ModelForm
from .models import Transaction, ProductType, Product
from user_management.models import Profile

        
class TransactionForm(ModelForm):
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.value():
            field.widget.attrs({'class': 'form-control'})
        return form

    class Meta:
        model = Transaction
        fields = ('amount',)
        

class ItemForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # widgets = {'owner': forms.HiddenInput()}
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].disabled = True
     