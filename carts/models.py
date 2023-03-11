from django.db import models
from pharmastore.models import Product, Variation
from accounts.models import Account

# Create your models here.
# Cart models is like a container stores a cart instance
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id


"""Cartitem are items present in the cart at the given moment depends on cart with the "cart" variable 
and products are connected with the "product" variable"""
class CartItem(models.Model):
    variation = models.ManyToManyField(Variation, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return self.product