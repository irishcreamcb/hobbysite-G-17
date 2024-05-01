from django.urls import path

from .views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('blog/articles', ArticleListView.as_view(), name='list'),
    path('blog/article/<int:pk>', ArticleDetailView.as_view(), name='detail')
]


app_name = 'blog'