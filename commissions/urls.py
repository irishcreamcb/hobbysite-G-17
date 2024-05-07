from django.urls import path 
from .views import CommissionListView, CommissionDetailView, CommissionUpdateView, CommissionCreateView, JobApplicationCreateView


urlpatterns = [
    path('commissions/list', CommissionListView.as_view(), name='commission-list'),
    path('commissions/detail/<pk>', CommissionDetailView.as_view(), name='commission-detail'), 
    path('commissions/<pk>/edit', CommissionUpdateView.as_view(), name='commission-update'), 
    path('commissions/add', CommissionCreateView.as_view(), name='commission-create'), 
    path('commissions/job/apply', JobApplicationCreateView.as_view(), name='job-application'),
]

app_name = 'commissions'