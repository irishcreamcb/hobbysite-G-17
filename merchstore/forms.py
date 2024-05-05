from django import forms
from django.forms import ModelForm
from .models import Transaction, ProductType, Product

        
class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_status']


class ItemForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["owner"].disabled = True
        



