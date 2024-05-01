from django.urls import path, include
from .views import ItemList, ItemDetail

urlpatterns = [
    path('merchstore/items', ItemList.as_view(), name="list"),
    path('merchstore/item/<int:pk>', ItemDetail.as_view(), name="item-detail")
]

app_name = 'merchstore'
