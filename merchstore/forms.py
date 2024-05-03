from django import forms
from .models import Transaction, ProductType

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'


class CreateForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.TextField()
    price = forms.DecimalField(max_digits=7, decimal_places=2)
    Product_Type = forms.ModelChoiceField(queryset=ProductType.objects.all())
