from django.shortcuts import render
from django.views import View
from user_management.models import Profile
from commissions.models import Commission
from blog.models import Article as BlogArticle
from wiki.models import Article as WikiArticle

class IndexView(View):
    def get(self, request, *args, **kwargs):
        ctx = {}
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            ctx["blog_articles"] = BlogArticle.objects.filter(author=profile)
            ctx["wiki_articles"] = WikiArticle.objects.filter(author=profile)
            ctx["commissions"] = Commission.objects.filter(creator=profile)
        return render(request, "index.html", ctx)

