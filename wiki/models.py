from django.db import models
from django.urls import reverse
from user_management.models import *

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Article categories"


class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL)
    category = models.ForeignKey(ArticleCategory, null=True, on_delete=models.SET_NULL)
    entry = models.TextField()
    header_image = models.ImageField(upload_to="images/")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)
    
    def get_absolute_url(self):
        return reverse('wiki:detail', args=[str(self.pk)])

    class Meta:
        ordering = ["-created_on"]

class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]