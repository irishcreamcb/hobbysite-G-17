from django.contrib import admin
from .models import Commission, Comment 


class CommissionInline(admin.TabularInline): 
    model = Commission


class CommentInline(admin.TabularInline): 
    model = Comment 


class CommissionAdmin(admin.ModelAdmin): 
    model = Commission
    inlines = [CommentInline,]

    list_display = ['title']


admin.site.register(Commission, CommissionAdmin)