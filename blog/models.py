from django.db import models
from django.urls import reverse


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
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)

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