from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('placeorder/', views.PlaceOrder, name="placeorderpage"),
    path('paymentpage/', views.PaymentOrder, name="paymentpage"),
    path('order_complete/', views.OrderComplete, name="ordercomplete"),
]