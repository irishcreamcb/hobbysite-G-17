from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Article, ArticleCategory
from .forms import ArticleForm


class ArticleListView(ListView):
    template_name = 'blog_list.html'

    def get_queryset(self):
        return Article.objects.exclude(author__user=self.request.user.id).order_by('category')
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_articles'] = Article.objects.filter(author__user=self.request.user.id)
        ctx['articles_logged_out'] = Article.objects.all().order_by('category')
        return ctx


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog_detail.html'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog_add.html'

    def get_success_url(self):
        return reverse_lazy('blog:list')


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog_edit.html'

    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk })