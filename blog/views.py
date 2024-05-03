from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Article, ArticleCategory
from .forms import ArticleForm


class ArticleListView(LoginRequiredMixin, ListView):
    model = ArticleCategory
    template_name = 'blog_list.html'


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'blog_detail.html'


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog_add.html'

    def get_success_url(self):
        return reverse_lazy('blog:list')


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog_edit.html'

    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={ 'pk': self.object.pk })