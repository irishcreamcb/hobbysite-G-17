from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Article, Profile
from .forms import ArticleForm, CommentForm


class ArticleListView(ListView):
    template_name = 'blog/blog_list.html'

    def get_queryset(self):
        return Article.objects.exclude(author__user=self.request.user.id).order_by('category')
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_articles'] = Article.objects.filter(author__user=self.request.user.id)
        ctx['articles_logged_out'] = Article.objects.all().order_by('category')
        return ctx


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        author = Article.objects.get(pk=self.object.pk).author
        ctx = super().get_context_data(**kwargs)
        ctx['related_articles'] = Article.objects.filter(author=author).exclude(id=self.object.pk)
        ctx['comment_form'] = CommentForm()
        ctx['comments'] = Article.objects.get(pk=self.object.pk).comments.all()
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


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/blog_add.html'

    def get_success_url(self):
        return reverse_lazy('blog:list')
    
    def get_form(self, form_class=None):
        profile = Profile.objects.get(user=self.request.user)
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        form.fields['author'].choices = [(profile.id, profile.display_name)]
        return form


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/blog_edit.html'

    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk })
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        form.fields['author'].disabled = True
        return form