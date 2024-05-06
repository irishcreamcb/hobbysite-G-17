from django.contrib import admin

from .models import Article, ArticleCategory


class ArticleInline(admin.TabularInline):
    model = Article
    list_display = ('title',
                    'entry',
                    'created_on',
                    'update_on',
                    'author',
                    'category')
    fieldsets = [
        (None, { 'fields': [('title',
                            'entry',
                            'created_on',
                            'update_on',
                            'author',
                            'category')] } ),
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


class ArticleCategoryAdmin(admin.ModelAdmin):
    model = ArticleCategory
    inlines = [ArticleInline,]


admin.site.register(ArticleCategory, ArticleCategoryAdmin)