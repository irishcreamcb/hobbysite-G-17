from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Product, Transaction, ProductType
from user_management import models as ProfileModel
from .forms import ItemForm, TransactionForm
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class ItemList(ListView):
    context_object_name = "list"
    model = Product
    template_name = "items_list.html"
    
    def get_queryset(self):
        sets = {
            'buy': Product.objects.exclude(owner_id__user=self.request.user),
            'own':Product.objects.filter(owner_id__user=self.request.user),    
        }        
        return sets


class ItemDetail(DetailView):
    model = Product
    template_name = "item_info.html"
    form_class = TransactionForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['Buyfrom'] = TransactionForm(
            
        )
        stock = Product.stock - amount
        # if (stock <= 0):
        #     return 
        return ctx


class ItemCreate(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ItemForm
    template_name = "item_create.html"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        owner = ProfileModel.Profile.objects.get(user=self.request.user)
        ctx['Addform'] = ItemForm(
            initial = {'owner':owner,}
        )
        return ctx
    
    
class ItemUpdate(UpdateView):
    model = Product
    template_name = "item_update.html"
    form_class = ItemForm

    def get_success_url(self) -> str:
        return reverse_lazy(
            'merchstore:item-detail', 
            args=[self.object.pk]
            )

class CartList(ListView):
    model = Transaction 
    template_name = "cart.html"


class TransactionList(ListView):
    model = Transaction
    template_name = "transaction.html"
    