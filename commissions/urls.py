from django.urls import path 
from .views import CommissionListView, CommissionDetailView, CommissionUpdateView, CommissionCreateView, JobApplicationCreateView


urlpatterns = [
    path('list', CommissionListView.as_view(), name='commission-list'),
    path('<int:pk>', CommissionDetailView.as_view(), name='commission-detail'), 
    path('<int:pk>/edit', CommissionUpdateView.as_view(), name='commission-update'), 
    path('add', CommissionCreateView.as_view(), name='commission-create'), 
    path('job/apply', JobApplicationCreateView.as_view(), name='job-application'),
]

app_name = 'commissions'