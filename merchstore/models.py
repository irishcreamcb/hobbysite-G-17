from django.db import models
from django.urls import reverse
from user_management import models as user_models



# Create your models here.
class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    def __str__(self):
        return self.name
    
    class Meta: 
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255)
    Product_Type = models.ForeignKey(
        'ProductType', 
        on_delete=models.SET_NULL,
        null=True,
        related_name='type'
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    owner = models.ForeignKey(
        user_models.Profile,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    stock = models.IntegerField()
    available = "AVAILABLE"
    no_stock = "OUT OF STOCK"
    sale = "ON SALE"
    product_status_choices = (
        (available, "Available"),
        (no_stock, "Out of Stock"),
        (sale, "On Sale")
    )
    product_status = models.CharField(max_length=12,
                              choices=product_status_choices,
                              default="AVAILABLE")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('merchstore:item-detail', args=[self.pk])

    class Meta: 
        ordering = ['name']


class Transaction(models.Model):
    buyer = models.ForeignKey(
        user_models.Profile, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='buyer'
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        related_name='purchased_product'
    )
    amount = models.IntegerField()
    cart = "ON CART"
    pay = "TO PAY"
    ship = "TO SHIP"
    receive = "TO RECEIVE"
    delivered = "DELIVERED"
    transaction_status_choices = (
        (cart, "On Cart"),
        (pay, "To Pay"),
        (ship, "To Ship"),
        (receive, "To Receive"),
        (delivered, "Delivered")
    )
    transaction_status = models.CharField(max_length=20,
                              choices=transaction_status_choices,
                              default="ON CART")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    
    

