from django.db import models
from django.urls import reverse

from user_management.models import Profile


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
    

class Article(models.Model):
    title = models.CharField(max_length=255)
    entry = models.TextField()
    header = models.ImageField(upload_to='images/')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.SET_NULL) 

    category = models.ForeignKey(
        ArticleCategory,
        null=True,
        on_delete=models.SET_NULL,
        related_name='article') 
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.pk])
    
    class Meta:
        ordering = ['-created_on']


class Comment(models.Model):
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.SET_NULL) 

    article = models.ForeignKey(
        Article,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments') 
    
    class Meta:
        ordering = ['created_on']