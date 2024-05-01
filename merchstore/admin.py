from django.contrib import admin
from .models import Product, ProductType

# Register your models here.

# Register your models here.
class ItemsInLine(admin.StackedInline):
    model = Product

class ProductDetails(admin.ModelAdmin):
    model = ProductType
    inlines = [ItemsInLine]


admin.site.register(ProductType, ProductDetails)