from django.urls import path

from .views import ProfileUpdateView

urlpatterns = [ 
    path('profile/<int:pk>', ProfileUpdateView.as_view(), name = 'profile-update')
]

app_name = 'user_management'
