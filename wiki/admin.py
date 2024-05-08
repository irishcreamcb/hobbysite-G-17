from django.contrib import admin

from .models import Article, ArticleCategory, Comment


class ArticleInline(admin.TabularInline):
    model = Article
    readonly_fields=('created_on', 'updated_on')


class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [ArticleInline,]
    class Meta:
        verbose_name_plural="Article categories"

class CommentAdmin(admin.ModelAdmin):
    model = Comment


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Comment, CommentAdmin)