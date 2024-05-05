from django.urls import path, include
from .views import ItemList, ItemDetail, ItemCreate, ItemUpdate, CartList, TransactionList

urlpatterns = [
    path('merchstore/items', ItemList.as_view(), name="list"),
    path('merchstore/item/<int:pk>', ItemDetail.as_view(), name="item-detail"),
    path('merchstore/item/add', ItemCreate.as_view(), name="item-add"),
    path('merchstore/item/<int:pk>/edit', ItemUpdate.as_view(), name="item-update"),
    path('merchstore/cart', CartList.as_view(), name="cart"),
    path('merchstore/transactions', TransactionList.as_view(), name="transaction-list")
]

app_name = 'merchstore'
