from django.contrib import admin
from .models import Product, ProductType

# Register your models here.

# Register your models here.
class ItemsInLine(admin.StackedInline):
    model = Product

class ProductDetails(admin.ModelAdmin):
    model = ProductType
    inlines = [ItemsInLine]

class ProductsAll(admin.ModelAdmin):
    model = Product
    search_fields = ['name']
    list_display = ['name']
    list_filter = ['owner', 'name', 'price']


admin.site.register(ProductType, ProductDetails)
admin.site.register(Product, ProductsAll)