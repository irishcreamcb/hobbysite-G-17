from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView

from .models import *
from .forms import CommentForm

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = '__all__'

    def get_form(self, form_class=None):
        profile = Profile.objects.get(user=self.request.user)
        form = super().get_form(form_class)
        form.fields['title'].widget.attrs.update({'class': 'form-control'})
        form.fields['author'].widget.attrs.update({'class': 'form-control'})
        form.fields['category'].widget.attrs.update({'class': 'form-control'})
        form.fields['entry'].widget.attrs.update({'class': 'form-control'})
        form.fields['header_image'].widget.attrs.update({'class': 'form-control'})
        form.fields['author'].choices = [(profile.id, profile.display_name)]
        return form

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['title'].widget.attrs.update({'class': 'form-control'})
        form.fields['author'].widget.attrs.update({'class': 'form-control'})
        form.fields['category'].widget.attrs.update({'class': 'form-control'})
        form.fields['entry'].widget.attrs.update({'class': 'form-control'})
        form.fields['header_image'].widget.attrs.update({'class': 'form-control'})
        form.fields['author'].disabled = True
        return form
    
class ArticleListView(ListView):
    template_name = 'wiki/article_list.html'
    context_object_name = 'all_articles'
    def get_queryset(self):
        return Article.objects.exclude(author__user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['my_articles'] = Article.objects.filter(author__user=self.request.user)
        return ctx

class ArticleDetailView(DetailView):
    template_name = 'wiki/article_detail.html'
    model = Article
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["article"] = Article.objects.get(pk=self.object.pk)
        ctx["read_more"] = Article.objects.exclude(pk=self.object.pk)
        ctx["form"] = CommentForm()
        ctx["comments"] = Article.objects.get(pk=self.object.pk).comments.all()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = Profile.objects.filter(user=request.user)[0]
            comment.article = Article.objects.get(pk=self.object.pk)
            comment.save()
            form = CommentForm()
        return self.get(self, request)