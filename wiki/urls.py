from django.urls import path, include
from .views import *

urlpatterns = [
    path('articles', ArticleListView.as_view(), name='list'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='detail'),
]

app_name = 'wiki'