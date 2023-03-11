from django.db import models
from accounts.models import Account
from pharmastore.models import Product, Variation

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    creasted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    
    def get_amount_paid_inr(self):
        return float("{:.2f}".format(self.amount_paid*81.52))

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phoneno = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_full_address(self):
        return f'{self.address_line_1} {self.address_line_2} {self.pin}'
    
    def get_tax_usd(self):
        return float("{:.2f}".format(self.tax*0.0125))
    
    def get_order_total(self):
        return float("{:.2f}".format(self.order_total))
    
    def get_order_total_usd(self):
        return float("{:.2f}".format(self.order_total*0.0125))
    
    def __str__(self):
        return self.first_name

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
    
    def get_product_price_usd(self):
        return float("{:.2f}".format(self.product_price*0.0125))
