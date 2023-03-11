from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = 'carts'

urlpatterns = [
    #Home page for the user
    path('', views.Cartpage, name="cartpage"),
    path('add_cart/<int:product_id>/', views.add_cart, name="add_cart_page"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name="remove_cart_page"),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name="remove_cart_item_page"),
    path('checkoutcart/', views.checkout_cart, name="checkout_cart"),
    ]