from django.urls import path, include
from .views import *

urlpatterns = [
    path('articles', ArticleListView.as_view(), name='list'),
    path('article/<int:pk>', article_detail, name='detail'),
    path('article/add', ArticleCreateView.as_view(), name='add'),
    path('article/<int:pk>/edit', ArticleUpdateView.as_view(), name='edit')
]

app_name = 'wiki'