from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phoneno', 'email', 'address_line_1', 'address_line_2', 'state', 'city', 'pin', 'note']
