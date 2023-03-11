from django.contrib import admin
from .models import Order, OrderProduct, Payment

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'get_full_name', 'phoneno', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    list_editable = ['status',]
    search_fields = ['order_number', 'first_name', 'last_name', 'phoneno', 'email']
    list_per_page = 15
    inlines = [OrderProductInline]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_method', 'amount_paid', 'status']

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'user' ,'payment', 'quantity', 'created_at', 'updated_at']
    list_filter = ['quantity', 'created_at']

# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Payment, PaymentAdmin)

