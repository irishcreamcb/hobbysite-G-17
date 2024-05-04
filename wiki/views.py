from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from .models import *
from .forms import CommentForm

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = '__all__'

    def get_form(self, form_class=None):
        profile = Profile.objects.get(user=self.request.user)
        form = super().get_form(form_class)
        form.fields['author'].choices = [(profile.id, profile.display_name)]
        return form

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['author'].disabled = True
        return form
    
class ArticleListView(ListView):
    template_name = 'wiki/article_list.html'
    context_object_name = 'all_articles'
    def get_queryset(self):
        return Article.objects.exclude(author__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_articles'] = Article.objects.filter(author__user=self.request.user)
        return context

def article_detail(request, pk):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.fields['entry']
            comment = form.save(commit=False)
            comment.author = Profile.objects.filter(user=request.user)[0]
            comment.article = Article.objects.get(pk=pk)
            comment.save()
            form = CommentForm()

    ctx = {
        'article': Article.objects.get(pk=pk),
        'read_more': Article.objects.exclude(pk=pk)[:2],
        'comment_form': form,
        'comments': Article.objects.get(pk=pk).comments.all()
    }

    return render(request, 'wiki/article_detail.html', ctx)
