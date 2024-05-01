from django.urls import path

from .views import ProfileUpdateView

urlpatterns = [ 
    path('/update', ProfileUpdateView.as_view(), name = 'profile-update')
]

app_name = 'user_management'