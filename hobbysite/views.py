from django.shortcuts import render
from django.views import View
from user_management.models import Profile
from commissions.models import Commission, Job, JobApplication
from merchstore.models import Product, Transaction
from blog.models import Article as BlogArticle
from wiki.models import Article as WikiArticle

class IndexView(View):
    def get(self, request, *args, **kwargs):
        ctx = {}
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            ctx["blog_articles"] = BlogArticle.objects.filter(author=profile)
            ctx["wiki_articles"] = WikiArticle.objects.filter(author=profile)
            ctx["commissions_created"] = Commission.objects.filter(creator=profile)
            ctx["commissions_joined"] = list(set([job.commission for job in [job_application.job for job_application in JobApplication.objects.filter(applicant=profile)]]))
            ctx["products_bought"] = list(set([transaction.product for transaction in Transaction.objects.filter(buyer=profile)]))
            ctx["products_sold"] = Product.objects.filter(owner=profile)
            
        return render(request, "index.html", ctx)

