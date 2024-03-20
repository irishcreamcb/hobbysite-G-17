from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Product, ProductType

# Create your views here.
class ItemList(ListView):
    model = Product
    template_name = "items_list.html"

class ItemDetail(DetailView):
    model = Product
    template_name = "item_info.html"