from django.urls import path, include
from .views import ItemList, ItemDetail, ItemCreate, ItemUpdate, CartList, TransactionList

urlpatterns = [
    path('items', ItemList.as_view(), name="list"),
    path('item/<int:pk>', ItemDetail.as_view(), name="item-detail"),
    path('item/add', ItemCreate.as_view(), name="item-add"),
    path('item/<int:pk>/edit', ItemUpdate.as_view(), name="item-update"),
    path('cart', CartList.as_view(), name="cart"),
    path('transactions', TransactionList.as_view(), name="transaction-list")
]

app_name = 'merchstore'
