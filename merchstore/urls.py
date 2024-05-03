from django.urls import path, include
from .views import ItemList, ItemDetail

urlpatterns = [
    path('merchstore/items', ItemList.as_view(), name="list"),
    path('merchstore/item/<int:pk>', ItemDetail.as_view(), name="item-detail"),
    path('/merchstore/item/add'),
    path('/merchstore/item/<int:pk>/edit',),
    path('/merchstore/cart',),
    path('/merchstore/transactions',)
]

app_name = 'merchstore'
