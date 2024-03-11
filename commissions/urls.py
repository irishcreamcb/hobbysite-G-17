from django.urls import path 
from .views import CommissionListView, CommissionDetailView 


urlpatterns = [
    path('commissions/list', CommissionListView.as_view(), name='commissions'),
    path('commission/<pk>', CommissionDetailView.as_view(), name='commission-detail')
]

app_name = 'commissions'