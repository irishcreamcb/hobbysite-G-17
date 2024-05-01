from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import ArticleCategory


class ArticleListView(ListView):
    model = ArticleCategory
    template_name = 'blog_list.html'


class ArticleDetailView(DetailView):
    model = ArticleCategory
    template_name = 'blog_detail.html'