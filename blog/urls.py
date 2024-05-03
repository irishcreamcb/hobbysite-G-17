from django.urls import path

from .views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView

urlpatterns = [
    path('blog/articles', ArticleListView.as_view(), name='list'),
    path('blog/article/<int:pk>', ArticleDetailView.as_view(), name='detail'),
    path('blog/article/add', ArticleCreateView.as_view(), name='add'),
    path('blog/article/<int:pk>/edit', ArticleUpdateView.as_view(), name='edit')
]


app_name = 'blog'