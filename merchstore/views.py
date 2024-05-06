from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Product, Transaction, ProductType
from user_management import models as ProfileModel
from user_management.models import Profile

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
    
    def get_user(self):
        user = ProfileModel.Profile.objects.get(user=self.request.user) 
        return user
    
    def get_context_data(self, **kwargs):
        item = self.get_object()
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            buyer = self.get_user()
            form = TransactionForm(
                initial={
                    'product': item,
                    'buyer': buyer,
                }
            )
        form = TransactionForm(
            initial={
                'product': item
            }
        )
        ctx['buy_form'] = form
        return ctx

    def dispatch(self, request, *args, **kwargs):
        item = self.get_object() 
        transaction_info = request.session.get('transaction_info')
        print("dispatch " + item.product_status)
        print(item.stock)
        if transaction_info:
            if self.get_user == item.owner:
                del request.session['transaction_info']
                return redirect('merchstore:list')
            
            buyer = self.get_user()
            amount = transaction_info['amount']
            form = TransactionForm()
            initial_transaction = form.save(commit=False)
            transaction = TransactionForm(self, initial_transaction, amount, buyer)
            transaction.save()
            item.save()
            del request.session['transaction_info']
            return redirect('merchstore:list')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        item = self.get_object()
        print("post " + item.product_status)
        print(item.stock)
        form = TransactionForm(request.POST)
        if form.is_valid():
            purchase_attempt = form.save(commit=False)
            amount = purchase_attempt.amount
            if request.user.is_authenticated: 
                buyer = self.get_user()
                transaction = self.make_transaction(purchase_attempt, item, amount, buyer)
                transaction.save()
                item.save()
                return redirect('merchstore:cart')
            else:
                request.session['transaction_info'] = {
                    'amount': transaction.amount
                }
                login_url = reverse('login') + '?next=' + request.get_full_path()
                return redirect(login_url)
        ctx = self.get_context_data(object=item, transaction_form=form)
        return self.render_to_response(ctx)
    
    def make_transaction(self, transaction, product, amount, user):
        transaction.product = product
        transaction.product_status = product.available 
        transaction.buyer = user
        transaction.amount = amount
        product.stock -= amount
        if product.stock <= 0:
            transaction.product_status = product.no_stock
        return transaction 


class ItemCreate(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ItemForm
    template_name = "item_create.html"
    
    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = Profile.objects.get(user=self.request.user)
        return initial 
     
    
class ItemUpdate(UpdateView):
    model = Product
    template_name = "item_update.html"
    form_class = ItemForm

    def form_valid(self, form):
        form.save()
        item = self.get_object()
        if item.stock == 0:
            print("in " + item.product_status)
            item.product_status = "OUT OF STOCK" 
        else: 
            item.product_status
        item.save()
        print("out " + item.product_status)
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('merchstore:item-detail', args=[self.object.pk])
    


class CartList(ListView):
    model = Transaction 
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = Profile.objects.get(user=self.request.user) 
        purchased = Transaction.objects.filter(buyer=user)
        sellers = Profile.objects.all()
        ctx['purchased_items'] = purchased
        ctx['all_sellers'] = sellers
        return ctx


class TransactionList(ListView):
    model = Transaction
    template_name = "transaction.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = Profile.objects.get(user=self.request.user) 
        sellers_items


    